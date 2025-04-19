import logging
import srt
from typing import Optional, List

from subtitle_translator.services.lmstudio_local_api import LMStudioLocalAPI
from subtitle_translator.utils.srt_handler import parse_srt_content

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SubtitleTranslator:
    def __init__(self):
        self.llm_api_client = LMStudioLocalAPI()
        if not self.llm_api_client.LMSTUDIO_API_URL or not self.llm_api_client.MODEL_ID:
            logger.error(
                "API LLM não configurada corretamente nas variáveis de ambiente. Verifique LMSTUDIO_API_URL e MODEL_ID.")
        else:
            logger.info("Cliente da API LMStudio inicializado.")

    def translate_srt_string(self, original_srt_string: str) -> Optional[str]:
        logger.info("Iniciando processo de tradução SRT...")

        original_subtitles: Optional[List[srt.Subtitle]] = parse_srt_content(original_srt_string)

        if original_subtitles is None:
            logger.error("Falha ao parsear o conteúdo SRT original. Abortando tradução.")
            return None

        if not original_subtitles:
            logger.warning("Arquivo SRT original está vazio ou não contém legendas válidas.")
            return ""

        translated_subtitles: List[srt.Subtitle] = []
        total_subs = len(original_subtitles)
        logger.info(f"Total de {total_subs} legendas para traduzir.")

        for i, sub in enumerate(original_subtitles):
            logger.info(f"Traduzindo legenda {i + 1}/{total_subs} (Index Original: {sub.index})...")

            original_content = sub.content
            translated_text = None

            if original_content and original_content.strip():
                try:
                    translated_text = self.llm_api_client.translate(original_content)

                    if translated_text is None:
                        logger.warning(
                            f"Falha ao traduzir o conteúdo da legenda {sub.index}. Usando conteúdo original.")
                        translated_text = original_content
                    elif not translated_text.strip():
                        logger.warning(
                            f"Tradução retornou texto vazio ou apenas espaços para legenda {sub.index}. Usando conteúdo original.")
                        translated_text = original_content
                    else:
                        logger.info(f"Legenda {sub.index} traduzida com sucesso.")
                        logger.debug(f"Original: {original_content.replace(chr(10), ' ')}")
                        logger.debug(f"Traduzido: {translated_text.replace(chr(10), ' ')}")

                except Exception as e:
                    logger.error(f"Erro inesperado ao tentar traduzir legenda {sub.index}: {e}", exc_info=True)
                    translated_text = original_content
            else:
                logger.info(f"Legenda {sub.index} possui conteúdo vazio ou apenas espaços. Mantendo original.")
                translated_text = original_content

            new_sub = srt.Subtitle(
                index=sub.index,
                start=sub.start,
                end=sub.end,
                content=translated_text,
                proprietary=sub.proprietary
            )
            translated_subtitles.append(new_sub)

        try:
            logger.info("Compondo o arquivo SRT final traduzido...")
            final_srt_string = srt.compose(translated_subtitles)
            logger.info("Arquivo SRT traduzido composto com sucesso.")
            return final_srt_string
        except Exception as e:
            logger.error(f"Erro ao compor o arquivo SRT final: {e}", exc_info=True)
            return None