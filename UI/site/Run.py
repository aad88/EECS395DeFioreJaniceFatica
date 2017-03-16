# native imports

# project imports

# external imports
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home_template():
	return render_template(
		'home'
	)

if __name__ == '__main__':
	app.run()
