Record multiple panes of the terminal using tmux and asciinema

```
tmux new -s claude-tekton-demo # Create a tmux session
tmux Ctr+B and % # Split the screen vertically
tmux Ctr+B and " # Split the screen horizontally
tmux Ctr+B and d # Dettach from the tmux session
asciinema rec -c "tmux attach -t claude-tekton-demo"
```
