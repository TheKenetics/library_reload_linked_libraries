bl_info = {
	"name": "Reload Linked Libraries",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (3, 0, 0),
	"location": "File > External Files > Reload All Linked Libraries",
	"description": "Allows to reload linked libraries in current Blend file.",
	"warning": "",
	"wiki_url": "",
	"category": "System"
}

import bpy
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences


## Operators
class RLL_OT_reload_all_linked_libraries(Operator):
	"""Reloads all linked libraries in this Blend file."""
	bl_idname = "rll.reload_all_linked_libraries"
	bl_label = "Reload All Linked Libraries"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context):
		return bpy.data.libraries

	def execute(self, context):
		for library in bpy.data.libraries:
			library.reload()
		
		self.report({"INFO"}, f"Reloaded all libraries.")

		return {'FINISHED'}


def get_enum_items(self, context):
	enum_list = []
	
	for index, library in enumerate(bpy.data.libraries):
		enum_list.append( (str(index), library.name, "") )
	
	return enum_list

class RLL_OT_reload_linked_library(Operator):
	"""Reloads a linked library in this Blend file."""
	bl_idname = "rll.reload_linked_library"
	bl_label = "Reload Linked Library..."
	bl_options = {'REGISTER'}

	library_index : EnumProperty(items=get_enum_items, name="Library")

	@classmethod
	def poll(cls, context):
		return bpy.data.libraries

	# Dialog invoke
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	def execute(self, context):
		library = bpy.data.libraries[int(self.library_index)]
		library.reload()
		
		self.report({"INFO"}, f"Reloaded {library.name}")
		
		return {'FINISHED'}


## Append to UI Helper Functions
def draw_func(self, context):
	layout = self.layout
	
	layout.separator()
	
	layout.operator(RLL_OT_reload_all_linked_libraries.bl_idname)
	layout.operator(RLL_OT_reload_linked_library.bl_idname)


## Register
classes = (
	RLL_OT_reload_all_linked_libraries,
	RLL_OT_reload_linked_library
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	## Append to UI
	bpy.types.TOPBAR_MT_file_external_data.append(draw_func)

def unregister():
	## Remove from UI
	bpy.types.TOPBAR_MT_file_external_data.remove(draw_func)
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
