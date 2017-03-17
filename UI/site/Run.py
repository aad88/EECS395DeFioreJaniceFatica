# native imports

# project imports

# external imports
from flask import Flask, render_template
app = Flask(__name__)

# template dictionary
TEMPLATE_DIC = {
	'Test Page': ('test', '/test', 'PoM TEST PAGE'),
	'Home': ('home', '/', 'Home - Presents of Mind'),
	'Login': ('login', '/login', 'Login - Presents of Mind')
}

# template dictionary entry index constants
TEMPLATE_DIC_NAME_ENTRY = 0
TEMPLATE_DIC_PATH_ENTRY = 1
TEMPLATE_DIC_PAGE_HEAD_ENTRY = 2

def create_nav_bar():
	nav_bar = []
	
	for name in TEMPLATE_DIC:
		path = TEMPLATE_DIC[name][TEMPLATE_DIC_PATH_ENTRY]
		nav_bar.append((name, path))
	
	return nav_bar

# EMPTY PAGE FOR TESTING
@app.route(TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_PATH_ENTRY])
def test_page_template():
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_NAME_ENTRY],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Test Page',
		page_header=TEMPLATE_DIC['Test Page'][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		
		# template-specific fields
		dummy=''
	)

@app.route(TEMPLATE_DIC['Home'][TEMPLATE_DIC_PATH_ENTRY])
def home_template():
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Home'][TEMPLATE_DIC_NAME_ENTRY],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Home',
		page_header=TEMPLATE_DIC['Home'][TEMPLATE_DIC_PAGE_HEAD_ENTRY],
		
		# template-specific fields
		dummy=''
	)

if __name__ == '__main__':
	app.run()

