from django.shortcuts import render
import os
import mimetypes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile



from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredFileLoader

from .models import Document, ChunkingStrategy, AIModel
from .serializers import DocumentUploadSerializer


class DocumentUploadView(APIView):
    """
    API endpoint for uploading documents, extracting text, and storing it.
    Supports various file types (TXT, PDF, DOCX) using LangChain loaders.
    """

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for file uploads.
        """

        serializer = DocumentUploadSerializer(data=request.data, context={'request': request})


        if serializer.is_valid():

            uploaded_file: UploadedFile = request.data.get('file')

            if not uploaded_file:

                return Response(
                    {"file": "No file was submitted. Please upload a file."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            temp_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

            try:
                with open(temp_file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
            except Exception as e:
                return Response(
                    {"error": f"Failed to save uploaded file temporarily: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            extracted_text = ""

            file_metadata = {
                "filename": uploaded_file.name,
                "file_size": uploaded_file.size,
                "content_type": uploaded_file.content_type,
            }

            try:

                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                loader = None


                match file_extension:
                    case '.pdf':
                        loader = PyPDFLoader(temp_file_path)
                    case '.docx':
                        loader = Docx2txtLoader(temp_file_path)
                    case '.txt':
                        loader = TextLoader(temp_file_path)
                    case _:

                        loader = UnstructuredFileLoader(temp_file_path)
                        # You might also want to check the MIME type for robustness
                        # mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                        # if mime_type and mime_type.startswith('text/'):
                        #     loader = TextLoader(temp_file_path)
                        # else:
                        #     loader = UnstructuredFileLoader(temp_file_path)

                if not loader:

                    raise ValueError(f"No suitable loader found for file type: {file_extension}")


                langchain_docs = loader.load()

                if not langchain_docs:

                    extracted_text = ""
                else:

                    extracted_text = "\n\n".join([doc.page_content for doc in langchain_docs])


                    if langchain_docs[0].metadata:
                        file_metadata.update(langchain_docs[0].metadata)

            except Exception as e:

                return Response(
                    {"error": f"Failed to extract text from file '{uploaded_file.name}': {e}",
                     "file_name": uploaded_file.name,
                     "file_type": uploaded_file.content_type},
                    status=status.HTTP_400_BAD_REQUEST
                )
            finally:

                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)


            chunking_strategie_instance = serializer.validated_data.get('chunking_strategie')
            ai_model_instance = serializer.validated_data.get('ai_model')

            document = Document.objects.create(
                content=extracted_text,
                metadata=file_metadata,
                chunking_strategie=chunking_strategie_instance,
                ai_model=ai_model_instance
            )


            response_serializer = DocumentUploadSerializer(document)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)