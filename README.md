# Gerador de documentos

Gera documentos Word a partir de um modelo `.docx` com marcadores `{{ campo }}` e um arquivo JSON por documento. É apropriado para contratos, propostas e comunicados que dependem de dados já validados em cadastro.

## Planejamento

1. Aprovar o modelo jurídico/comercial antes da automação.
2. Mapear campos obrigatórios e validar dados de entrada.
3. Gerar documentos em pasta de saída e submetê-los à revisão humana.
4. Só depois integrar com assinatura, e-mail ou armazenamento externo.

## Execução

```powershell
pip install -r requirements.txt
Copy-Item config.example.json config.json
python main.py --config config.json
python main.py --config config.json --apply
```

Sem `--apply`, o processo valida e exibe o plano, sem produzir documentos.
