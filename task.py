import time
from datetime import  datetime, date
from functools import partial

from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread


from flet import *


HEIGHT = 590
WIDTH = 280

controlCounter = 0

class TitleClass(UserControl):    
    def __init__(self):
        super().__init__()
        
    
    def _Title(self):
        return Text(
            value = "Task creator app",
            size = 15,
            weight = "bold",
        )      
        
    def _Time(self):
        return Row(
            alignment = MainAxisAlignment.CENTER,
            spacing = 0,
            controls = [
                Text(
                    value = "",
                    size = 50,
                    weight = "bold",
                ),
                Container(
                    padding = padding.only(top=16),
                    content = Text(
                            value = "",
                            size = 30,
                            weight = "bold",
                    ),                      
                ),                
            ]
        )
        
    def _Date(self):
        return Text(
            value = "",
            size = 11,
            weight = "w500",
        )
        
    
    def build(self):
        return Container(
            padding = padding.only(top=25),
            content = Column(
                horizontal_alignment = CrossAxisAlignment.CENTER,
                spacing = 0,
                controls= [
                    self._Title(),
                    self._Time(),
                    self._Date(),
                ],
            ),
        )
        
class TaskClass(UserControl):
    
    def __init__(self, is_visible:bool ,func):
        self.is_visible = is_visible
        self.func = func
        super().__init__()
        
    
    def _InputContainer(self, width:str, text:str, keyboard:KeyboardType):
        return Container(
            width = width,
            height = 50,
            bgcolor = 'white24',
            border_radius = 10,
            padding = 8,
            content = Column(
                spacing = 1,
                controls = [
                    Text(
                        value = text,
                        size = 9,
                        color = 'white',
                        weight = 'bold',
                    ),
                    TextField(
                        border_color = 'transparent',
                        height = 20,
                    ),    
                ],
            ),
        )
    
    def _SelectTime(self, width:str):
        return Container(
            width = width,
            height = 50,
            bgcolor = 'white24',
            border_radius = 10,
            content = Dropdown(
                height = 50,
                border_color = 'transparent',
                text_style = TextStyle(
                    size = 10,
                    color = "white",
                    weight = "bold",
                ),
                options = [
                    dropdown.Option('seconds'),
                    dropdown.Option('minutes'),
                    dropdown.Option('hours'),
                ],
            ),
        )
            
    def build(self):
        return Column(
            visible = self.is_visible,
            controls = [
                Text(
                    value = "Scheduler Task",
                    size = 15,
                    weight = 'bold',
                ),
                self._InputContainer(290, 'Tasks Description', KeyboardType.TEXT),
                Row(
                    alignment = MainAxisAlignment.START,
                    spacing = 5,
                    controls = [
                        self._InputContainer(80, 'Every', KeyboardType.NUMBER),
                        self._SelectTime(155),
                    ],
                ),
                Container(
                    alignment = alignment.center,
                    content = ElevatedButton(
                        on_click = partial(self.func),
                        bgcolor = 'blue900',
                        content = Text(
                            value = "Task",
                            size = 11,
                            weight = 'bold',
                            color = 'white',
                        ),
                        style = ButtonStyle(
                            shape = {
                                "": RoundedRectangleBorder(radius=8),
                            },
                            color = {
                                "": 'white',
                            },
                        ),   
                        height = 48,
                        width = 200,
                    ),  
                ),
            ],
        )  

class CreateTask(UserControl):
    def __init__(self, description:str, interval:float, duration:str):
        self.description = description
        self.interval = interval
        self.duration = duration
        super().__init__()
        
    def build(self):
        return Row(
            controls = [
                Container(
                    border_radius = 8,
                    padding = 12,
                    expand = True,
                    bgcolor = 'blue800',
                    content = Column(
                        spacing = 2,
                        controls = [
                            Text(
                                value = self.description,
                                size = 10,
                            ),
                            Text(
                                value = f"Every {self.interval} {self.duration}",
                                size = 9,
                            ),                               
                        ],
                    ),
                ),
                Container(
                    alignment = alignment.center_right,
                    animate = animation.Animation(1000, 'ease'),
                    content = Row(
                        alignment = "end",
                        spacing = 0,
                        controls = [
                            IconButton(
                                icon = icons.NOTIFICATIONS,
                                icon_size = 19,
                                opacity = 0,
                                animate_opacity = 300,
                                icon_color = "red500",
                                scale = transform.Scale(scale=1),
                                animate_scale = animation.Animation(900),                            
                            )
                        ]
                    )
                ),
            ], 
            #on_hover = 
        )
    
    
    
def main(page: Page):
    
    def new_task(e):
        if _top_container.height == HEIGHT * 0.7:
            _top_container.content.controls[2].controls[0].visible = False
            
            _top_container.height = HEIGHT * 0.3
            _top_container.content.controls[2].controls[0].update()
            time.sleep(0.1)
            _top_container.update()
        else:
            _top_container.height = HEIGHT * 0.7
            _top_container.content.controls[2].controls[0].visible = True
            _top_container.update()
            time.sleep(0.1)
            _top_container.content.controls[2].controls[0].update()
    
    def _notify(num:int):
        _center_container.content.controls[num].controls[0].controls[1].content.controls[0].scale = 1.5 
        _center_container.content.controls[num].controls[0].controls[1].content.controls[0].opacity = 1        
        _center_container.content.controls[num].controls[0].controls[1].content.controls[0].update()
        
        time.sleep(2)
        
        _center_container.content.controls[num].controls[0].controls[1].content.controls[0].scale = 1 
        _center_container.content.controls[num].controls[0].controls[1].content.controls[0].opacity = 0        
        _center_container.content.controls[num].controls[0].controls[1].content.controls[0].update()
        
    def _set_task(e):
        
        global controlCounter
        
        description = _top_container.content.controls[2].controls[0].controls[1].content.controls[1].value
        _top_container.content.controls[2].controls[0].controls[1].content.controls[1].value = ''
        interval = _top_container.content.controls[2].controls[0].controls[2].controls[0].content.controls[1].value
        _top_container.content.controls[2].controls[0].controls[2].controls[0].content.controls[1].value = ''
        duration = _top_container.content.controls[2].controls[0].controls[2].controls[1].content.value
        _top_container.content.controls[2].controls[0].controls[2].controls[1].content.value = ''
        
        _center_container.content.controls.append(
            CreateTask(description, interval, duration)
        )
        _center_container.update()
        
        scheduler = BackgroundScheduler()         
        if duration == 'seconds':
            scheduler.add_job(_notify, trigger="interval", args=[controlCounter], seconds=int(interval))
        if duration == 'minutes':
            scheduler.add_job(_notify, trigger="interval", args=[controlCounter], minutes=int(interval))
        if duration == 'hours':
            scheduler.add_job(_notify, trigger="interval", args=[controlCounter], hours=int(interval))
        scheduler.start()
        controlCounter +=1
        new_task(None)
        
    def _current_data():
        while True:
            now = datetime.now()
            current_date = now.strftime("%A %B, %d")
            current_time = now.strftime("%H:%M")
            current_second = now.strftime(":%S")
            _top_container.content.controls[0].controls[0].content.controls[1].controls[0].value = current_time
            _top_container.content.controls[0].controls[0].content.controls[1].controls[1].content.value = current_second
            _top_container.content.controls[0].controls[0].content.controls[2].value = current_date
            
            _top_container.content.controls[0].controls[0].content.update()
            
            sleep(1)
            
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    # Contenedor superior 
    _top_container = Container(
        height = HEIGHT * 0.3,
        width = WIDTH,
        gradient = LinearGradient(
            begin = alignment.bottom_left,
            end = alignment.top_right,
            colors = ["blue400", "blue600", "blue700", "blue900"],
        ),
        border_radius = border_radius.only(
            topLeft=35, 
            topRight=35, 
            bottomLeft=42, 
            bottomRight=42,
            ),
        animate = Animation(
            duration = 1000,
            curve = "elasticOut"
        ),  
        padding = 15,
        alignment = alignment.center,
        content = Column(
            horizontal_alignment = CrossAxisAlignment.CENTER,            
            controls = [
                TitleClass(),
                Container(padding=5),
                TaskClass(False, _set_task),
            ],    
        ),
    )
        
    # contenedor del cuerpo
    _center_container = Container(
        width = WIDTH,
        height = HEIGHT * 0.95, 
        padding = padding.only(
                    top = HEIGHT * 0.32, 
                    right = 10, 
                    left = 10, 
                    bottom = 5
                ),
        content=Column(
            scroll = 'auto',
            alignment = MainAxisAlignment.CENTER,
            controls = []
        ),
    )
    
    # Contenedor inferior con boton de despliegue
    _button_task = Column(
        alignment = MainAxisAlignment.END,
        horizontal_alignment = "center",
        width = WIDTH,
        controls = [
            Container(
                height = 6,
                width = WIDTH * 0.35,
                bgcolor = "blue900",
                border_radius = 25,
                animate = 900,
                on_click = lambda e: new_task(e),
                content = None,
            ),
        ],
    )
    
    # contenedor principal
    _main_container = Container(
        height = HEIGHT,
        width = WIDTH,
        bgcolor = "black",
        border_radius = 35,
        padding = 6,
        content = Stack(
            width = WIDTH,
            height = HEIGHT,
            controls = [
                _center_container,
                _top_container,
                _button_task,
            ],
            
        ),
    )
            
    page.add(_main_container)        
    page.update()
    
    threading.Thread(target=_current_data, daemon=True).start()    


if __name__ == '__main__':
    app(target=main)