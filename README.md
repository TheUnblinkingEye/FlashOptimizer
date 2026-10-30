# ⚡ FlashOptimizer

FlashOptimizer é um utilitário open-source moderno desenvolvido em Python para limpar, atualizar e acelerar sistemas Windows de forma cirúrgica. Ele combina o poder das ferramentas nativas da Microsoft com uma interface gráfica (GUI) responsiva e elegante.

## ✨ Funcionalidades
- **Modern Dark UI:** Interface responsiva construída em CustomTkinter.
- **Mapeamento Inteligente de Drivers:** Limpa versões legadas duplicadas do `DriverStore` sem causar instabilidade.
- **Upgrade Automatizado:** Integração com o `Winget` para atualizar todos os componentes vitais e softwares instalados em lote.
- **Deep Windows Update Cleanup:** Reduz o tamanho da pasta oculta `WinSxS` usando rotinas seguras do `DISM`.
- **Explicação Dinâmica de Symlinks:** Seção didática explicando como salvar gigabytes de ferramentas de desenvolvimento movendo os dados para o segundo drive.

## 🚀 Como Executar
1. Instale as dependências:
   
   pip install -r requirements.txt
   
2. Execute o script como Administrador (obrigatório para manipulação de drivers):

   python main.py
   

## 📜 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.