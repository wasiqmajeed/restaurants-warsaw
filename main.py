from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///restaurants-warsaw.db"
db.init_app(app)


class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(250), nullable=False)

    def get_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()
@app.route('/add', methods=['POST'])
def add_restaurant():
    #Used postmaster to add the restaurants
    restaurant = Restaurants(id=request.form.get('id'),
                             name=request.form.get('name'),
                             rating=request.form.get('rating'),
                             address=request.form.get('address'),
                             type=request.form.get('type'))
    db.session.add(restaurant)
    db.session.commit()
    return jsonify(success={"success":"Restaurant added successfully"})


@app.route('/all-restaurants')
def get_all_restaurants():
    all_restaurants = db.session.execute(db.select(Restaurants)).scalars().all()
    restaurant_list = [data.get_dict() for data in all_restaurants]
    return jsonify(restaurants = restaurant_list)

@app.route('/food-type')
def food_type():
    restaurant_type = request.args.get('type')
    restaurant_list = db.session.execute(db.select(Restaurants).where(Restaurants.type == restaurant_type)).scalars().all()
    if restaurant_list:
        return jsonify(restaurant=[place.get_dict() for place in restaurant_list])
    else:
        return "No Match found, please try another kind of food."


if __name__ == "__main__":
    app.run(debug=True)
