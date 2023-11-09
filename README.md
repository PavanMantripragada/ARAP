# Dependencies

`pip install numpy`
`pip install open3d`

# Instructions to Run

`cd <repo>`
`python scripts/interactive_editor.py`

Enter a segment id to select the part you want to edit in the command prompt

Now an interactive window opens with your mesh
The code sets the editable segment blue and rest black

In the GUI

Pressing Shift : should highlight all selectable points in magenta

You should only select mesh vertices in blue region

Pressing Shift + left click drag: You can drag a rectangle to select the points

the selected points are shown in green

You can perform multiple selections by changing views and the final selection is just the union of all

You can only unselect one point at a time, you can do that by Shift+left click on that particular point

Pressing Shift + right click drag : To move the selected points 

Once released, the mesh deforms and if you find the deformation satisfactory close the GUI and it saves the file

