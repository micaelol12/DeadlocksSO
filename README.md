# DeadlocksSO ☠️

## Sobre

O projeto tem como intuito simular o deadlock entre recursos e processos

**Aluno**: Micael Luan Conti  
**Disciplina**: Sistemas Operacionais  
**Instituição**: Furb

### Estratégia para Correção do deadlock
- Redução de grafo;
- Seta que chega: pedido de recurso
- Seta que sai: recurso alocado

## Intalação
```
pip install tkinter 
```
## Run
```
python main.py
```

## Build

```
python -m PyInstaller main.py --windowed
```

## Tutorial

- Recursos e Processos são nós
- Para adicionar um nó pressione o respectivo botão (recurso || processo) na barra de tarefas e clique na tela com o botão esquerdo
- Para adicionar uma aresta clique em um nó e depois em outro com o botão esquerdo
- Para remover uma aresta/processo clique com o botão direito
- Para editar um recurso clique com o botão direito

## Exemplos

### Exemplo 1 (com Deadlock ☠️)
![Alt Text](./examples/gif/exemplo1.gif)

### Exemplo 2 (sem Deadlock 😎)
![Alt Text](./examples/gif/exemplo2.gif)

## TODO List

Lista de itens a serem adicionais

1. Melhorar Layout
2. Rever algorimo de Deadlock
3. Sistema de desfazer e refazer
