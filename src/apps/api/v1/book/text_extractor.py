import os
import io
from ebooklib import epub, ITEM_DOCUMENT
from docx import Document
from lxml import etree
from bs4 import BeautifulSoup
from django.core.files.uploadedfile import InMemoryUploadedFile

import tempfile
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

class TextExtractor:
    def __init__(self, uploaded_file: InMemoryUploadedFile):
        if not isinstance(uploaded_file, InMemoryUploadedFile):
            raise ValueError("Expected an InMemoryUploadedFile instance.")
        
        self.file = uploaded_file
        self.file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    def extract_text(self):
        if self.file_extension == '.epub':
            return self._extract_text_from_epub()
        elif self.file_extension == '.txt':
            return self._extract_text_from_txt()
        elif self.file_extension == '.docx':
            return self._extract_text_from_docx()
        elif self.file_extension == '.fb2':
            return self._extract_text_from_fb2()
        else:
            raise ValueError(f"Unsupported file format: {self.file_extension}")



    def _extract_text_from_epub(self):
        # Создаем временный файл из InMemoryUploadedFile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as temp_file:
            # Записываем содержимое InMemoryUploadedFile в временный файл
            temp_file.write(self.file.read())
            temp_file.flush()
            
            # Читаем EPUB из временного файла
            book = epub.read_epub(temp_file.name)
        
        # Удаляем временный файл после использования
        os.unlink(temp_file.name)

        text = []
        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                content = item.get_content().decode('utf-8', errors='ignore')  # Игнорировать ошибки декодирования
                soup = BeautifulSoup(content, 'html.parser')
                text.append(soup.get_text(separator='\n'))
        
        return '\n'.join(text)

    def _extract_text_from_txt(self):
        return self.file.read().decode('utf-8', errors='ignore')

    def _extract_text_from_docx(self):
        doc = Document(self.file)
        return '\n'.join([para.text for para in doc.paragraphs])

    def _extract_text_from_fb2(self):
        tree = etree.parse(source=self.file, parser=etree.XMLParser())
        root = tree.getroot()
        namespace = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
        text_elements = root.xpath('//fb2:body//fb2:p', namespaces=namespace)
        
        # Декодируем байтовые строки в обычные строки
        text_list = [etree.tostring(element, encoding='unicode', method='text') for element in text_elements]
        
        return '\n'.join(text_list)
  