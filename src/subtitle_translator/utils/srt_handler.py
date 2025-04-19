import srt
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_srt_content(srt_string: str) -> Optional[List[srt.Subtitle]]:
    try:
        logger.info("Iniciando parsing do conteúdo SRT...")
        subtitle_generator = srt.parse(srt_string)
        subtitles = list(subtitle_generator)
        logger.info(f"Parsing concluído. {len(subtitles)} legendas encontradas.")

        return subtitles

    except srt.SRTParseError as e:
        logger.error(f"Erro de parsing SRT: Formato inválido ou corrompido. Detalhes: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado durante o parsing SRT: {e}")
        return None