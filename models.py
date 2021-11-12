# Author: Guilherme Crepaldi
"""
Modelos de dados do ENEM.
Dataclasses que representam as entidades principais.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Candidato:
    """Um participante do ENEM."""
    id: Optional[int] = None
    ano: Optional[int] = None
    faixa_etaria: Optional[int] = None
    sexo: Optional[str] = None
    estado_civil: Optional[int] = None
    cor_raca: Optional[int] = None
    nacionalidade: Optional[int] = None
    situacao_conclusao: Optional[int] = None
    tipo_escola: Optional[int] = None
    treineiro: Optional[bool] = None

    # Notas
    nota_cn: Optional[float] = None
    nota_ch: Optional[float] = None
    nota_lc: Optional[float] = None
    nota_mt: Optional[float] = None
    nota_redacao: Optional[float] = None

    @property
    def nota_media(self) -> Optional[float]:
        """
        Media simples das 5 notas.
        Se alguma nota for None, retorna None.
        """
        notas = [
            self.nota_cn,
            self.nota_ch,
            self.nota_lc,
            self.nota_mt,
            self.nota_redacao,
        ]
        if None in notas:
            return None
        return round(sum(notas) / len(notas), 2)

    @property
    def nota_media_sem_redacao(self) -> Optional[float]:
        """Media das 4 provas objetivas (sem redacao)."""
        notas = [
            self.nota_cn,
            self.nota_ch,
            self.nota_lc,
            self.nota_mt,
        ]
        if None in notas:
            return None
        return round(sum(notas) / len(notas), 2)


@dataclass
class Escola:
    """Escola de origem do candidato."""
    id: Optional[int] = None
    nome: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    situacao_funcionamento: Optional[int] = None
    tipo_dependencia: Optional[int] = None
    tipo_localizacao: Optional[int] = None


@dataclass
class Notas:
    """Notas de um candidato em uma edicao do ENEM."""
    ano: Optional[int] = None
    id_candidato: Optional[int] = None

    # Provas objetivas
    nota_cn: Optional[float] = None  # Ciencias da Natureza
    nota_ch: Optional[float] = None  # Ciencias Humanas
    nota_lc: Optional[float] = None  # Linguagens e Codigos
    nota_mt: Optional[float] = None  # Matematica

    # Redacao
    nota_redacao: Optional[float] = None

    # Nota por competencia da redacao
    competencia_1: Optional[int] = None
    competencia_2: Optional[int] = None
    competencia_3: Optional[int] = None
    competencia_4: Optional[int] = None
    competencia_5: Optional[int] = None

    @property
    def nota_media(self) -> Optional[float]:
        """Media simples de todas as 5 notas."""
        notas = [
            self.nota_cn,
            self.nota_ch,
            self.nota_lc,
            self.nota_mt,
            self.nota_redacao,
        ]
        if None in notas:
            return None
        return round(sum(notas) / len(notas), 2)
