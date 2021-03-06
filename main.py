import pyglet
from pyglet.gl import *
from random import *

window = pyglet.window.Window(1024,768)

#colors (pairs of 3)
square_white = (255,255,255,255,255,255,255,255,255,255,255,255)
square_black = (0,0,0,0,0,0,0,0,0,0,0,0)

size = 50
tiles = [[0 for col in range(size)] for row in range(size)]

for i in xrange(0, size):
	for j in xrange(0, size):
		tiles[i][j] = randint(0,1)

def get_value(r, c):
	try:
		r = int(tiles[r][c] or 0)
		return r
	except IndexError:
		return 0


def add_neighbors(row, col):
	total = 0

	neighborValues =[
		[row-1, col-1],
		[row-1, col],
		[row-1, col+1],
		[row, col-1],
		[row, col+1],
		[row+1, col-1],
		[row+1, col],
		[row+1, col+1]
	]

	for item in neighborValues:
		total += get_value(item[0], item[1])

	return total


def game_of_life(t, state):
	# is currently alive
	if state == 1: 
		# any live cell with fewer than two live neighbors dies - under-population
		if t < 2: 
			return 0
		# any live cell with two or three live neighbors lives on to the next generation
		if t == 2 or t == 3: 
			return 1
		# any live cell with more than three live neighbors dies - overcrowding
		if t > 3: 
			return 0
	#is currently dead
	else: 
		# any dead cell with exactly three live neighbors becomes a live cell - reproduction
		if t == 3: 
			return 1
		else:
			return 0


def update(dt):
	updateList = []
	for row in xrange(0, size):
		for col in xrange(0, size):
			total = add_neighbors(row, col)
			result = game_of_life(total, tiles[row][col])
			if result != tiles[row][col]:
				updateList.append([row, col])

	for item in updateList:
		if tiles[item[0]][item[1]] == 1:
			tiles[item[0]][item[1]] = 0
		else:
			tiles[item[0]][item[1]] = 1


@window.event
def on_draw():
    for row in xrange(0, size):
    	for col in xrange(0, size):
    		if tiles[row][col] == 1:
    			color = square_black
    		else:
    			color = square_white

    		#top left, top right, bottom left, bottom right
    		verts = (col*50, window.height-(row*50), (col*50)+50, window.height-(row*50), 
    				(col*50)+50, window.height-(row*50) - 50, (col*50), window.height-(row*50) - 50)  
    		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,('v2i', verts),('c3B', color))



if __name__ == "__main__":
	pyglet.clock.schedule_interval(update, 1/1)
	pyglet.app.run()