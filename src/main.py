# subtitle-translator/main.py

import argparse
import logging
import sys
from pathlib import Path

from subtitle_translator.core.translator import SubtitleTranslator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_translation(input_path: Path, output_path: Path):
    """
    Executa o fluxo principal de leitura, tradução e escrita do arquivo SRT.

    Args:
        input_path: Objeto Path para o arquivo SRT de entrada.
        output_path: Objeto Path para o arquivo SRT de saída.
    """
    logger.info(f"Iniciando tradução do arquivo: {input_path}")

    try:
        original_srt_content = input_path.read_text(encoding='utf-8')
        logger.info(f"Arquivo '{input_path}' lido com sucesso (UTF-8).")
    except FileNotFoundError:
        logger.error(f"Erro: Arquivo de entrada não encontrado em '{input_path}'")
        sys.exit(1) # Termina o script com código de erro
    except UnicodeDecodeError:
        logger.warning(f"Falha ao decodificar '{input_path}' como UTF-8. Tentando latin-1...")
        try:
            original_srt_content = input_path.read_text(encoding='latin-1')
            logger.info(f"Arquivo '{input_path}' lido com sucesso (latin-1).")
        except Exception as e:
            logger.error(f"Erro ao ler o arquivo de entrada '{input_path}' com UTF-8 ou latin-1: {e}", exc_info=True)
            sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado ao ler o arquivo de entrada '{input_path}': {e}", exc_info=True)
        sys.exit(1)

    if not original_srt_content:
        logger.warning(f"O arquivo de entrada '{input_path}' está vazio. Nada a traduzir.")
        try:
            output_path.write_text("", encoding='utf-8')
            logger.info(f"Arquivo de saída vazio criado em '{output_path}'.")
            sys.exit(0) # Termina com sucesso
        except Exception as e:
            logger.error(f"Erro ao criar arquivo de saída vazio '{output_path}': {e}", exc_info=True)
            sys.exit(1)

    try:
        translator = SubtitleTranslator()
        if not translator.llm_api_client.LMSTUDIO_API_URL:
             logger.error("Falha ao inicializar o tradutor: Configuração da API LLM ausente ou inválida.")
             logger.error("Verifique as variáveis de ambiente LMSTUDIO_API_URL e MODEL_ID no arquivo .env")
             sys.exit(1)

        logger.info("Iniciando chamada para a API de tradução...")
        translated_srt_content = translator.translate_srt_string(original_srt_content)

    except Exception as e:
        logger.error(f"Erro durante o processo de tradução: {e}", exc_info=True)
        sys.exit(1)

    if translated_srt_content is None:
        logger.error("O processo de tradução falhou e não retornou conteúdo. Arquivo de saída não será criado.")
        sys.exit(1)
    elif not translated_srt_content:
         logger.warning("O processo de tradução retornou conteúdo vazio. Verifique os logs do tradutor.")

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(translated_srt_content, encoding='utf-8')
        logger.info(f"Tradução concluída com sucesso! Arquivo salvo em: {output_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar o arquivo de saída em '{output_path}': {e}", exc_info=True)
        sys.exit(1)

def main():
    """
    Função principal que configura o argparse e chama a lógica de tradução.
    """
    parser = argparse.ArgumentParser(
        description="Traduz um arquivo de legenda SRT usando uma API LLM local.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        type=Path,
        help="Caminho para o arquivo .srt de entrada."
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        type=Path,
        help="Caminho para salvar o arquivo .srt traduzido."
    )

    args = parser.parse_args()

    run_translation(args.input, args.output)


if __name__ == "__main__":
    main()
