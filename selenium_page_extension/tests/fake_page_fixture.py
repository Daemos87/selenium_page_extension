import os

import pytest


@pytest.fixture
def fake_html():
    frame_path = os.path.abspath("./frame.html")
    page_path = os.path.abspath("./page.html")

    fake_frame = """
    <html>
               <head>
               </head>
               <body>
                   <button id='button1' onclick='document.getElementById("button1").textContent="premuto";'> 
                    click me
                   </button>
                   
               </body>
           </html>
    """
    fake_page = f"""
           <html>
               <head>
               </head>
               <body>
                   <iframe id="frame" src="{frame_path}"></iframe>
                   <button id="button" onclick="document.getElementById('button').textContent='premuto';"> 
                        click me
                   </button>
                   <div id="e">AAA</div>
                   <div id="e">bbb</div>
                   <div id="e">ccc</div>
                   <div id="e">ddd</div>
               </body>
           </html>
           """

    with open(f"{page_path}", "w") as pag, open(f"{frame_path}", "w") as frame:
        pag.write(fake_page)
        frame.write(fake_frame)
    yield page_path
    os.remove(f"{os.path.abspath('page.html')}")
    os.remove(f"{os.path.abspath('frame.html')}")
