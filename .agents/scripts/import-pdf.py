import sys
import os
import re
from markitdown import MarkItDown

def padronizar_texto(texto):
    # 1. Remover cabeçalhos da Federação
    texto = re.sub(
        r'\x0c?\s*FEDERAÇÃO CEARENSE DE ORIENTAÇÃO'
        r'(?:\s*\n\s*Fundada em [^\n]+)?'
        r'(?:\s*\n\s*(?:de Orientação,\s*)?sob o\s*CNPJ:[^\n]+)?',
        '',
        texto
    )
    
    # 2. Remover rodapés da Federação (URL, páginas ~ X/Y ~ ou X/Y e data/hora opcional) de forma independente por linha
    texto = re.sub(r'(?m)^\s*www\.fecori\.org\.br\s*$', '', texto)
    texto = re.sub(r'(?m)^\s*(?:~\s*)?\d+\s*/\s*\d+\s*(?:~\s*)?$', '', texto)
    texto = re.sub(r'(?m)^\s*\d{2}/\d{2}/\d{2,4}\s+\d{2}:\d{2}\s*$', '', texto)
    
    # 3. Remover espaços duplos ou múltiplos entre palavras (preservando indentação de início de linha)
    texto = re.sub(r'(?<=\S)[ \t]{2,}', ' ', texto)
    
    # 4. Remover marcas de quebra de página (\x0c) residuais
    texto = texto.replace('\x0c', '')

    # 5. Capítulos: CAPÍTULO IV - DAS... -> ## CAPÍTULO IV - DAS...
    # Evita duplicar o ## se já tiver
    texto = re.sub(r'(?m)^(?!#+ )(CAPÍTULO\s+[IVXLCDM\d]+.*?)$', r'## \1', texto)
    
    # 6. Artigos: Art. 1º - O campeonato... -> **Art. 1º** – O campeonato...
    def normalize_artigo(match):
        num = match.group(1)
        suffix = match.group(2) or ''
        content = match.group(3)
        if suffix in ['o', '°']:
            suffix = 'º'
        return f"**Art. {num}{suffix}** – {content}"
        
    texto = re.sub(r'(?m)^Art\.\s*(\d+)([ºo°]?)\s*[-–—]\s*(.*)$', normalize_artigo, texto)
    
    # 7. Parágrafo único: Parágrafo Único - ... -> > **Parágrafo único:** ...
    # Suporta variações de acentuação e maiúsculas/minúsculas
    texto = re.sub(r'(?m)^Parágrafo\s*[uUüúÚ]n[ií]co\s*[-–—:]\s*(.*)$', r'> **Parágrafo único:** \1', texto)
    
    # 8. Parágrafo 1º - ... -> > **Parágrafo 1º:** ...
    def normalize_paragrafo_num(match):
        num = match.group(1)
        suffix = match.group(2) or ''
        content = match.group(3)
        if suffix in ['o', '°']:
            suffix = 'º'
        # Adiciona o ordinal se for de 1 a 9 e não tiver
        if not suffix and int(num) < 10:
            suffix = 'º'
        return f"> **Parágrafo {num}{suffix}:** {content}"
        
    texto = re.sub(r'(?m)^Parágrafo\s*(\d+)([ºo°]?)\s*[-–—:]\s*(.*)$', normalize_paragrafo_num, texto)
    
    # 9. Incisos: a) Blabla -> >> **a)** Blabla
    # Geralmente letras minúsculas seguidas de )
    texto = re.sub(r'(?m)^([a-z])\)\s*(.*)$', r'>> **\1)** \2', texto)
    
    # 10. Colapsar múltiplas linhas em branco seguidas (mais de 2 newlines)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    
    return texto.strip()

def main():
  if len(sys.argv) < 2:
    print("Uso: python import-pdf.py <caminho_do_pdf> [caminho_do_markdown_saida]")
    sys.exit(1)

  pdf_path = sys.argv[1]
  if not os.path.exists(pdf_path):
    print(f"Erro: Arquivo {pdf_path} não encontrado.")
    sys.exit(1)

  if len(sys.argv) >= 3:
    out_path = sys.argv[2]
  else:
    out_path = os.path.splitext(pdf_path)[0] + ".md"

  print(f"Convertendo {pdf_path} usando MarkItDown...")
  try:
    md = MarkItDown()
    result = md.convert(pdf_path)
    markdown_raw = result.text_content

    print("Aplicando regras de padronização jurídica...")
    markdown_padronizado = padronizar_texto(markdown_raw)

    with open(out_path, "w", encoding="utf-8") as f:
      f.write(markdown_padronizado)

    print(f"Sucesso! Arquivo salvo em: {out_path}")
  except Exception as e:
    print(f"Erro na conversão: {e}")
    sys.exit(1)

if __name__ == "__main__":
    main()
