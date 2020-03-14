from plotille import Canvas

c = Canvas(width=40, height=20)
c.rect(0.1, 0.1, 0.6, 0.6)
c.line(0.1, 0.1, 0.6, 0.6)
c.line(0.1, 0.6, 0.6, 0.1)
c.line(0.1, 0.6, 0.35, 0.8)
c.line(0.35, 0.8, 0.6, 0.6)
print(c.plot())
