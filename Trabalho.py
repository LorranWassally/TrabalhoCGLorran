import tkinter as tk

# Função para desenhar o plano cartesiano
def desenhar_plano(canvas):
    canvas.create_line(500, 0, 500, 1000, fill="black", width=2)  # Eixo Y
    canvas.create_line(0, 500, 1000, 500, fill="black", width=2)  # Eixo X
    for i in range(0, 1000, 50):
        canvas.create_line(i, 495, i, 505, fill="black")  # Marcas no eixo X
    for i in range(0, 1000, 50):
        canvas.create_line(495, i, 505, i, fill="black")  # Marcas no eixo Y

# Função para adicionar pontos ao plano
def adicionar_ponto(canvas, x, y):
    ponto = canvas.create_oval(500 + x * 25 - 5, 500 - y * 25 - 5, 500 + x * 25 + 5, 500 - y * 25 + 5, fill="red")
    texto = canvas.create_text(500 + x * 25, 500 - y * 25 - 10, text=f'({x},{y})', fill="black")
    pontos.append((ponto, texto, x, y))

# Função para atualizar o plano com novos pontos
def atualizar_plano():
    limpar_pontos_preenchidos()
    x = int(entry_x.get())
    y = int(entry_y.get())
    adicionar_ponto(canvas, x, y)

# Função para deletar pontos do plano
def deletar_ponto():
    limpar_pontos_preenchidos()
    x = int(entry_x.get())
    y = int(entry_y.get())
    for ponto, texto, px, py in pontos:
        if px == x and py == y:
            canvas.delete(ponto)
            canvas.delete(texto)
            pontos.remove((ponto, texto, px, py))
            break

# Algoritmo de Bresenham para gerar pontos
def bresenham(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    if dx > dy:
        err = dx / 2.0
        while x0 != x1:
            points.append((x0, y0))
            err -= dy
            if err < 0:
                y0 += sy
                err += dx
            x0 += sx
    else:
        err = dy / 2.0
        while y0 != y1:
            points.append((x0, y0))
            err -= dx
            if err < 0:
                x0 += sx
                err += dy
            y0 += sy
    points.append((x1, y1))  # Adiciona o ponto final
    return points

# Função para desenhar linhas entre os pontos
def desenhar_pontos_linha():
    limpar_pontos_preenchidos()
    for linha in linhas_desenhadas:
        canvas.delete(linha)
    linhas_desenhadas.clear()
    
    for i in range(len(pontos) - 1):
        p1 = (pontos[i][2], pontos[i][3])
        p2 = (pontos[i + 1][2], pontos[i + 1][3])
        for x, y in bresenham(p1[0], p1[1], p2[0], p2[1]):
            ponto = canvas.create_oval(500 + x * 25 - 2, 500 - y * 25 - 2, 500 + x * 25 + 2, 500 - y * 25 + 2, fill="blue")
            linhas_desenhadas.append(ponto)

# Função para desenhar círculos usando o algoritmo de Bresenham
def bresenham_circulo(x_center, y_center, radius):
    points = []
    x = 0
    y = radius
    d = 3 - 2 * radius
    while x <= y:
        points.extend([
            (x_center + x, y_center + y),
            (x_center - x, y_center + y),
            (x_center + x, y_center - y),
            (x_center - x, y_center - y),
            (x_center + y, y_center + x),
            (x_center - y, y_center + x),
            (x_center + y, y_center - x),
            (x_center - y, y_center - x)
        ])
        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1
    return points

# Função para desenhar círculos
def desenhar_circulo():
    limpar_pontos_preenchidos()
    for linha in linhas_desenhadas:
        canvas.delete(linha)
    linhas_desenhadas.clear()

    x_center = pontos[-1][2]
    y_center = pontos[-1][3]
    radius = int(entry_radius.get())
    
    for x, y in bresenham_circulo(x_center, y_center, radius):
        ponto = canvas.create_oval(500 + x * 25 - 2, 500 - y * 25 - 2, 500 + x * 25 + 2, 500 - y * 25 + 2, fill="green")
        linhas_desenhadas.append(ponto)

# Função para desenhar elipses usando o algoritmo de Bresenham
def bresenham_elipse(x_center, y_center, a, b):
    points = []
    x = 0
    y = b
    d1 = b * b - a * a * b + 0.25 * a * a
    while (b * b * x) < (a * a * y):
        points.append((x_center + x, y_center + y))
        points.append((x_center - x, y_center + y))
        points.append((x_center + x, y_center - y))
        points.append((x_center - x, y_center - y))
        
        if d1 < 0:
            d1 += 2 * b * b * x + 3 * b * b
        else:
            d1 += 2 * b * b * x - 2 * a * a * y + 2 * a * a
            y -= 1
        x += 1

    d2 = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
    while y >= 0:
        points.append((x_center + x, y_center + y))
        points.append((x_center - x, y_center + y))
        points.append((x_center + x, y_center - y))
        points.append((x_center - x, y_center - y))
        
        if d2 > 0:
            d2 += -2 * a * a * y + 3 * a * a
        else:
            d2 += 2 * b * b * x - 2 * a * a * y + 2 * a * a
            x += 1
        y -= 1
    return points

# Função para desenhar elipses
def desenhar_elipse():
    limpar_pontos_preenchidos()
    for linha in linhas_desenhadas:
        canvas.delete(linha)
    linhas_desenhadas.clear()

    x_center = pontos[-1][2]
    y_center = pontos[-1][3]
    a = int(entry_radius.get())  # Semi-eixo maior
    b = a // 2  # Semi-eixo menor

    for x, y in bresenham_elipse(x_center, y_center, a, b):
        ponto = canvas.create_oval(500 + x * 25 - 2, 500 - y * 25 - 2, 500 + x * 25 + 2, 500 - y * 25 + 2, fill="purple")
        linhas_desenhadas.append(ponto)

# Função para desenhar Bézier de grau 2
def bezier2(p1, p2, p3, num_points=100):
    points = []
    for t in range(num_points + 1):
        t /= num_points
        x = (1 - t) ** 2 * p1[0] + 2 * (1 - t) * t * p2[0] + t ** 2 * p3[0]
        y = (1 - t) ** 2 * p1[1] + 2 * (1 - t) * t * p2[1] + t ** 2 * p3[1]
        points.append((round(x), round(y)))
    return points

# Função para desenhar Bézier entre todos os pontos
def desenhar_bezier():
    limpar_pontos_preenchidos()
    for linha in linhas_desenhadas:
        canvas.delete(linha)
    linhas_desenhadas.clear()

    for i in range(len(pontos) - 2):
        p1 = (pontos[i][2], pontos[i][3])
        p2 = (pontos[i + 1][2], pontos[i + 1][3])
        p3 = (pontos[i + 2][2], pontos[i + 2][3])
        for x, y in bezier2(p1, p2, p3):
            ponto = canvas.create_oval(500 + x * 25 - 2, 500 - y * 25 - 2, 500 + x * 25 + 2, 500 - y * 25 + 2, fill="orange")
            linhas_desenhadas.append(ponto)

# Função para desenhar polígonos
def desenhar_poligono():
    limpar_pontos_preenchidos()
    for linha in linhas_desenhadas:
        canvas.delete(linha)
    linhas_desenhadas.clear()

    if len(pontos) < 4:
        return  # Necessita de pelo menos 4 pontos

    for i in range(len(pontos)):
        p1 = (pontos[i][2], pontos[i][3])
        p2 = (pontos[(i + 1) % len(pontos)][2], pontos[(i + 1) % len(pontos)][3])
        for x, y in bresenham(p1[0], p1[1], p2[0], p2[1]):
            ponto = canvas.create_oval(500 + x * 25 - 2, 500 - y * 25 - 2, 500 + x * 25 + 2, 500 - y * 25 + 2, fill="cyan")
            linhas_desenhadas.append(ponto)

# Função para verificar se um ponto está dentro do polígono usando o algoritmo de ray-casting
def ponto_dentro_poligono(ponto, poligono):
    x, y = ponto
    n = len(poligono)
    dentro = False
    p1x, p1y = poligono[0]
    for i in range(n + 1):
        p2x, p2y = poligono[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        dentro = not dentro
        p1x, p1y = p2x, p2y
    return dentro

# Lista para armazenar os pontos preenchidos
pontos_preenchidos = []

# Função para preencher os pontos dentro ou fora do polígono
def preencher():
    limpar_pontos_preenchidos()
    x = int(entry_fill_x.get())
    y = int(entry_fill_y.get())
    fill_color = "yellow"

    # Obter as coordenadas do polígono
    poligono = [(p[2], p[3]) for p in pontos]

    # Verifica se o ponto está dentro do polígono
    if ponto_dentro_poligono((x, y), poligono):
        # Desenhar pontos amarelos dentro do polígono
        for i in range(-500, 500):  # Considerando a área total
            for j in range(-500, 500):
                if ponto_dentro_poligono((x + i, y + j), poligono):
                    ponto = canvas.create_oval(500 + (x + i) * 25 - 1, 500 - (y + j) * 25 - 1, 
                                                500 + (x + i) * 25 + 1, 500 - (y + j) * 25 + 1, fill=fill_color)
                    pontos_preenchidos.append(ponto)
    else:
        # Desenhar pontos fora do polígono
        for i in range(-500, 500):  # Considerando a área total
            for j in range(-500, 500):
                if not ponto_dentro_poligono((x + i, y + j), poligono):
                    ponto = canvas.create_oval(500 + (x + i) * 25 - 1, 500 - (y + j) * 25 - 1, 
                                                500 + (x + i) * 25 + 1, 500 - (y + j) * 25 + 1, fill=fill_color)
                    pontos_preenchidos.append(ponto)

# Função para limpar pontos preenchidos
def limpar_pontos_preenchidos():
    for ponto in pontos_preenchidos:
        canvas.delete(ponto)
    pontos_preenchidos.clear()


# Configuração da janela principal
root = tk.Tk()
root.title("Plano Cartesiano com Tkinter")

# Configuração do canvas
canvas = tk.Canvas(root, width=1000, height=1000, bg="white")
canvas.grid(row=0, column=0, rowspan=8)

# Desenhar o plano cartesiano
desenhar_plano(canvas)

# Lista para armazenar os pontos
pontos = []
linhas_desenhadas = []  # Lista para armazenar referências das linhas desenhadas

# Adicionar pontos de exemplo
adicionar_ponto(canvas, -19, -17)
adicionar_ponto(canvas, -10, -15)
adicionar_ponto(canvas, 10, -8)
adicionar_ponto(canvas, 12, 14)


# Campos de entrada para coordenadas
label_x = tk.Label(root, text="X:")
label_x.grid(row=0, column=1, padx=10, pady=5, sticky="e")
entry_x = tk.Entry(root)
entry_x.grid(row=0, column=2, padx=10, pady=5)

label_y = tk.Label(root, text="Y:")
label_y.grid(row=1, column=1, padx=10, pady=5, sticky="e")
entry_y = tk.Entry(root)
entry_y.grid(row=1, column=2, padx=10, pady=5)

# Campo para especificar o raio do círculo
label_radius = tk.Label(root, text="Raio:")
label_radius.grid(row=2, column=1, padx=10, pady=5, sticky="e")
entry_radius = tk.Entry(root)
entry_radius.grid(row=2, column=2, padx=10, pady=5)

# Campo de entrada para preenchimento
label_fill_x = tk.Label(root, text="X Preenchimento:")
label_fill_x.grid(row=3, column=1, padx=10, pady=5, sticky="e")
entry_fill_x = tk.Entry(root)
entry_fill_x.grid(row=3, column=2, padx=10, pady=5)

label_fill_y = tk.Label(root, text="Y Preenchimento:")
label_fill_y.grid(row=4, column=1, padx=10, pady=5, sticky="e")
entry_fill_y = tk.Entry(root)
entry_fill_y.grid(row=4, column=2, padx=10, pady=5)

# Botões para as funcionalidades
button_add = tk.Button(root, text="Adicionar Ponto", command=atualizar_plano)
button_add.grid(row=5, column=1, padx=10, columnspan=2, pady=5)

button_delete = tk.Button(root, text="Deletar Ponto", command=deletar_ponto)
button_delete.grid(row=6, column=1, padx=10, columnspan=2, pady=5)

button_draw_line = tk.Button(root, text="Desenhar Linhas", command=desenhar_pontos_linha)
button_draw_line.grid(row=7, column=1, padx=10, columnspan=2, pady=5)

button_draw_circle = tk.Button(root, text="Desenhar Círculo", command=desenhar_circulo)
button_draw_circle.grid(row=5, column=2, padx=10, columnspan=2, pady=5)

button_draw_elipse = tk.Button(root, text="Desenhar Elipse", command=desenhar_elipse)
button_draw_elipse.grid(row=6, column=2, padx=10, columnspan=2, pady=5)

button_draw_bezier = tk.Button(root, text="Desenhar Bézier", command=desenhar_bezier)
button_draw_bezier.grid(row=7, column=2, padx=10, columnspan=2, pady=5)

button_draw_polygon = tk.Button(root, text="Desenhar Polígono", command=desenhar_poligono)
button_draw_polygon.grid(row=5, column=3, padx=10, columnspan=2, pady=5)

button_fill = tk.Button(root, text="Preencher", command=preencher)
button_fill.grid(row=6, column=3, padx=10, columnspan=2, pady=5)

# Iniciar o loop principal do Tkinter
root.mainloop()