====Abertura da virtual machine====
-python -m virtual <nome_da_pasta>
==> ATIVACAO
./<nome_da_pasta>/Scripts/activate

==>Esse ambiente virtual não possui nenhuma biblioteca:
pip list #=> ver as bibliotecas instaladas
pip install ==> instalar novas bibliotecas

==> FORCA UMA BIBLIOTECA EM ESPECIFICO
pip install requests==<versao_desejada>

ATUALIZAR O PIP:
python -m pip install --upgrade pip



==> PASSANDO OUTRA VERSÃO DO PYTHON
python -m virtual -p <pasta_do_python> <nome_da_pasta>




==> RODANDO JUPYTER:
-start virtual env 
-pip3 install notebook
-pip3 install jupyter
---> jupyter notebook # for start jupyter in chrome 

