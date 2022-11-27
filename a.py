from __future__ import annotations
from dataclasses import dataclass
import time

class Maze:
    START = -1
    END = 9
    WALL = 1
    OPEN = 0
    def __init__(self):
        self.map: list[list[int]] = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                     [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                                     [1,0,-1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,0,1],
                                     [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
                                     [1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,0,0,9,1,0,1],
                                     [1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,1],
                                     [1,0,1,1,1,1,1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
                                     [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1],
                                     [1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,0,0,0,1,0,1],
                                     [1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
                                     [1,0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
                                     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        self.END_POS: Position = self.find_pos(self.END)
        self.START_POS: Position = self.find_pos(self.START)
        
    def find_pos(self, key) -> Position:
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[0])):
                if (self.get_location(Position(x, y)) == key):
                    return Position(x, y)
                
    def get_location(self, pos: Position) -> Position:
        return self.map[pos.y][pos.x]
    
    def print(self, path: list[Node] = None):
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[0])):
                value = self.get_location(Position(x, y))
                if path != None:
                    if check_list(Node(Position(x, y)), path):
                        if value == self.START:
                            print('\x1b[0;30;44m ' + '2' + ' \x1b[0m', end='')
                            continue
                        elif value == self.END:
                            print('\x1b[0;30;45m ' + '2' + ' \x1b[0m', end='')
                            continue
                        else:
                            print('\x1b[0;30;42m ' + '2' + ' \x1b[0m', end='')
                            continue
                if value == self.WALL:
                    print('\x1b[0;37;40m ' + str(value) + ' \x1b[0m', end='')
                elif value == self.OPEN:
                    print('\x1b[0;30;47m ' + str(value) + ' \x1b[0m', end='')
                elif value == self.START:
                    print('\x1b[0;30;44m' + str(value) + ' \x1b[0m', end='')
                elif value == self.END:
                    print('\x1b[0;30;45m ' + str(value) + ' \x1b[0m', end='')
            print()
                

@dataclass
class Position:
    x: int
    y: int
    
    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

class Node:
    def __init__(self, pos: Position, parent: Node = None):
        self.pos: Position = pos
        self.parent: Node = parent
        self.h: int = self.h()
        self.g: int = 0 if parent == None else self.g()
        self.f: int = self.f()
        
    def h(self) -> int:
        return abs(self.pos.x - maze.END_POS.x) + abs(self.pos.y - maze.END_POS.y)
    
    def g(self) -> int:
        return self.parent.g + 1
    
    def f(self) -> int:
        return self.h + self.g

def check_list(child: Node, lst: list[Node]) -> bool:
    for node in lst:
        if node.pos == child.pos:
            return True

def get_node_in_list(child: Node, lst: list[Node]) -> Node:
    for node in lst:
        if node.pos == child.pos:
            return node

def astar():
    while open_list:
        time.sleep(0.1)
        print(chr(27) + '[2J')
        maze.print(closed_list)
        current_node: Node = open_list[0]
        for node in open_list:
            if node.f < current_node.f:
                current_node = node 
        
        closed_list.append(current_node)
        open_list.remove(current_node)

        child_nodes: list[Node] = [Node(Position(current_node.pos.x + 1, current_node.pos.y), current_node),
                    Node(Position(current_node.pos.x - 1, current_node.pos.y), current_node),
                    Node(Position(current_node.pos.x, current_node.pos.y + 1), current_node),
                    Node(Position(current_node.pos.x, current_node.pos.y - 1), current_node)]
        
        for child in child_nodes:
            if child.pos == maze.END_POS:
                print('FOUND END NODE')
                closed_list.append(child)
                return
            if maze.get_location(child.pos) == 1 or check_list(child, closed_list):
                continue
            if not check_list(child, open_list):
                open_list.append(child)
            else:
                node: Node = get_node_in_list(child, open_list)
                if child.g < node.g:
                    open_list.remove(node)
                    open_list.append(child)
    
    print("COULD NOT FIND END NODE")

def trace_path():
    path: list[Node] = [closed_list[-1]]
    while path[-1].g != 0:
        path.append(path[-1].parent)
    
    path.reverse()
    print(chr(27) + '[2J')
    maze.print(path)


maze: Maze = Maze()

open_list: list[Node] = [Node(maze.START_POS)]
closed_list: list[Node] = []

maze.print()

astar()

trace_path()
