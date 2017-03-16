# native imports

# project imports

# external imports
from flask import Flask, render_template
app = Flask(__name__)

# template dictionary
TEMPLATE_DIC = {
	'Home': ('home', '/'),
	'Login': ('login', '/login')
}

def create_nav_bar():
	nav_bar = []
	
	for name in TEMPLATE_DIC:
		url = TEMPLATE_DIC[name][1]
		print(url)
		nav_bar.append((name, url))
		print(nav_bar)
	
	return nav_bar

@app.route(TEMPLATE_DIC['Home'][1])
def home_template():
	return render_template(
		# template name, from dictionary
		TEMPLATE_DIC['Home'][0],
		
		# common fields
		nav_bar=create_nav_bar(),
		current_nav='Home',
		
		# template-specific fields
		page_header='Presents of Mind'
	)

if __name__ == '__main__':
	app.run()

