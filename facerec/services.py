from compreface import CompreFace
from compreface.service import RecognitionService
from compreface.collections import FaceCollection
from compreface.collections.face_collections import Subjects
from .models import Estudante, AppConfig
import json
from enum import Enum

class EstadoMaquinaAprendizadoEnum(Enum):
    TREINADA = 1
    NAO_TREINADA = 0

class MaquinaAprendizado:
    config = AppConfig.objects.first() # pega a primeira config.
    compre_face: CompreFace
    recognition: RecognitionService
    face_collection: FaceCollection
    subjects: Subjects

    def __init__(self) -> None:
        if (self.config is None):
            raise Exception ('Configuração do framework de reconhecimento não realizada')
    
        domain = self.config.get_domain()
        port = self.config.get_port()
        api_key = self.config.get_api_key()
        compre_face = CompreFace(domain, str(port))
        recognition = compre_face.init_face_recognition(api_key)
        self.face_collection = recognition.get_face_collection()
        self.subjects = recognition.get_subjects()

    def esta_treinada(self) -> bool:
        return len(self.subjects.list()) > 0       

    def quantidade_treinada(self) -> int:
        #print (self.subjects.list()['subjects'])
        #print(str(len(self.subjects.list()['subjects'])))
        return len(self.subjects.list()['subjects'])
    
class ReconhecimentoFace:
    maquina_aprendizado: MaquinaAprendizado
    FOTO_PATH = "http://localhost:7777"

    def __init__(self, maquina_aprendizado: MaquinaAprendizado) -> None:
        self.maquina_aprendizado = maquina_aprendizado

    def limpar(self) -> None:
        self.maquina_aprendizado.subjects.delete_all()

    def treinar(self, estudantes:[Estudante]) -> None:
        if self.maquina_aprendizado.quantidade_treinada() > 0:
            self.limpar()

        for estudante in estudantes:
            if estudante.foto and hasattr(estudante.foto, 'url'):
                imagem_path = self.FOTO_PATH+estudante.foto.url
                individuo = str(estudante.registro) + ":" + estudante.nome + " " + estudante.sobrenome            
                self.maquina_aprendizado.face_collection.add(imagem_path, individuo)

    def reconhecer (self, imagem_path: str):
        if self.maquina_aprendizado.recognition.get_face_collection():
            service: RecognitionService = self.maquina_aprendizado.recognition.recognize(image_path=imagem_path)
            data = json.load(service)
            for idade in data['result'][0]['age'][0]:
                print (idade["__value__"])
        
