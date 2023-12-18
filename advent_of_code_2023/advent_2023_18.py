with open('18.txt', 'r') as f:
    heat_loss_map = [[int(n) for n in line.strip()] for line in f.readlines()]

