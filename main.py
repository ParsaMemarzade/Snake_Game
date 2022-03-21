from random import randint
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window

class SnakePart(Widget):
    pass

class GameScreen(Widget):
    step_size = 40
    move_x = 0
    move_y = 0
    snake_parts = []
    score = 0

    def new_game(self):
        remove_list=[]
        for child in self.children:
            if isinstance(child,SnakePart):
                remove_list.append(child)
        for child in remove_list:
              self.remove_widget(child)      

        self.snake_parts = []
        self.move_x = 0
        self.move_y = 0
        self.score = 0
        head = SnakePart()
        self.snake_parts.append(head)
        self.add_widget(head)
        pass

    def on_touch_up(self, touch):
        dx = touch.x-touch.opos[0]
        dy = touch.y-touch.opos[1]
        if abs(dx) > abs(dy):
            self.move_y = 0
            if dx > 0:
                self.move_x = self.step_size

            else:
                self.move_x = - self.step_size

        else:
            self.move_x = 0
            if dy > 0:
                self.move_y = self.step_size

            else:
                self.move_y = -self.step_size

    def check_cliding(self, wid1, wid2):
        if wid1.x >= wid2.right:
            return 0
        if wid2.x >= wid1.right:
            return 0
        if wid1.y >= wid2.top:
            return 0
        if wid2.y >= wid1.top:
            return 0
        return 1

    def frame(self, *args):
       last_x = self.snake_parts[-1].x
       last_y = self.snake_parts[-1].y
       food = self.ids.food
       for i,part in enumerate(self.snake_parts):
            if i==0:
                continue
            part.new_x=self.snake_parts[i-1].x
            part.new_y=self.snake_parts[i-1].y

       for part in self.snake_parts[1:]:
            part.x=part.new_x
            part.y=part.new_y 

       head=self.snake_parts[0]
       head.x+=self.move_x
       head.y+=self.move_y
       for part in self.snake_parts[1:]:
           if self.check_cliding(part,head):
               self.score=0
               self.ids.score_label.text="Score: "+str(self.score)
               self.new_game()

       if not self.check_cliding(self,head):
           self.score=0
           self.ids.score_label.text="Score: "+str(self.score)
           self.new_game()
            
    
       if self.check_cliding(food,head):
           self.score+=1
           self.ids.score_label.text="Score: "+str(self.score)
           food.x = randint(0,Window.width-food.width)
           food.y = randint(0,Window.height-food.height)
           new_part=SnakePart()
           new_part.x=last_x
           new_part.y=last_y
           self.snake_parts.append(new_part)
           self.add_widget(new_part)
           
class mainApp(App):
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.frame,0.25)


mainApp().run()