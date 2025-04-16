#!/bin/bash

dir_path=$1
server_script=$2

original_dir=$(pwd)


first_dir=$(echo $dir_path | cut -d '/' -f 1)


report_file="relatorio_${first_dir}.md"
server_output_file="server_output_${first_dir}.log"

file_a="${dir_path}/a.txt"
file_b="${dir_path}/b.txt"

if [ -f "$file_a" ]; then
  size_a_bytes=$(stat -c %s "$file_a")
  size_a_kbytes=$(du -k "$file_a" | cut -f1)
else
  size_a_bytes="Arquivo não encontrado"
  size_a_kbytes="Arquivo não encontrado"
fi

if [ -f "$file_b" ]; then
  size_b_bytes=$(stat -c %s "$file_b")
  size_b_kbytes=$(du -k "$file_b" | cut -f1)
else
  size_b_bytes="Arquivo não encontrado"
  size_b_kbytes="Arquivo não encontrado"
fi

echo "# Relatorio do Grupo ( $first_dir )" > "$report_file"

echo "" >> "$report_file"
echo " - Copiando config.ini" >> "$report_file"
cd "$dir_path" || { echo "Erro ao acessar o diretório $dir_path"; exit 1; }

echo "- Iniciando o servidor: $server_script" >>  "$original_dir/$report_file"


python3 -u "$server_script" > "$original_dir/$server_output_file" 2>&1 &
server_pid=$!

echo " - Servidor iniciado com PID: $server_pid" >> "$original_dir/$report_file"
echo " - Saída do servidor salva em: $server_output_file" >> "$original_dir/$report_file"
echo "" >> "$original_dir/$report_file"


#iretório original
cd "$original_dir" || { echo "Erro ao voltar para o diretório original"; exit 1; }

echo "## Arquivos do Grupo" >> "$report_file"
echo "" >> "$report_file"

echo "- Arquivo a.txt - Bytes: $size_a_bytes, KBytes: $size_a_kbytes" >> "$report_file"
echo "- Arquivo b.txt - Bytes: $size_b_bytes, KBytes: $size_b_kbytes" >> "$report_file"
echo "" >> "$report_file"

echo "## Execucao do cliente" >> "$report_file"
echo "" >> "$report_file"

echo "### get a.txt" >> "$report_file"
echo '```' >> "$report_file"
python3 myclient.py a.txt | tee -a "$report_file"
echo '```' >> "$report_file"

echo "### get b.txt" >> "$report_file"
echo '```' >> "$report_file"
python3 myclient.py b.txt | tee -a "$report_file"
echo '```' >> "$report_file"

echo "Encerrando o servidor com PID: $server_pid"
kill $server_pid
echo "Servidor encerrado." >> "$report_file"

echo "" >> "$report_file"
echo "## Comentarios" >> "$report_file"