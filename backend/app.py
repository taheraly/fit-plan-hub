from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Plan

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitplanhub.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# --- AUTHENTICATION ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_pw, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "role": new_user.role}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = create_access_token(identity=user.username)
        return jsonify({"token": token, "role": user.role})
    return jsonify({"message": "Invalid credentials"}), 401

# --- NEW: SOCIAL FEATURES ---
@app.route('/trainers', methods=['GET'])
@jwt_required()
def get_all_trainers():
    current_username = get_jwt_identity()
    current_user = User.query.filter_by(username=current_username).first()
    
    # Get all trainers
    trainers = User.query.filter_by(role='trainer').all()
    output = []
    
    for t in trainers:
        # Check if we already follow them
        is_following = t in current_user.followed
        output.append({
            "id": t.id,
            "username": t.username,
            "is_following": is_following
        })
    return jsonify(output)

@app.route('/follow/<int:trainer_id>', methods=['POST'])
@jwt_required()
def follow_trainer(trainer_id):
    current_username = get_jwt_identity()
    current_user = User.query.filter_by(username=current_username).first()
    trainer = User.query.get(trainer_id)
    
    if not trainer or trainer.role != 'trainer':
        return jsonify({"message": "Trainer not found"}), 404
    
    if trainer not in current_user.followed:
        current_user.followed.append(trainer)
        db.session.commit()
        return jsonify({"message": f"You are now following {trainer.username}!"})
    
    return jsonify({"message": "Already following"})

# --- EXISTING ROUTES ---
@app.route('/create_plan', methods=['POST'])
@jwt_required()
def create_plan():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    
    if user.role != 'trainer':
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.json
    new_plan = Plan(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        duration=data['duration'],
        trainer_id=user.id
    )
    db.session.add(new_plan)
    db.session.commit()
    return jsonify({"message": "Plan created!"}), 201

@app.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    
    followed_trainers = user.followed.all()
    feed_plans = []
    
    for trainer in followed_trainers:
        for plan in trainer.plans_created:
            is_purchased = plan in user.subscribed_plans
            
            plan_data = {
                "id": plan.id,
                "title": plan.title,
                "trainer": trainer.username,
                "price": plan.price,
                "is_purchased": is_purchased
            }
            
            if is_purchased:
                plan_data["description"] = plan.description
            else:
                plan_data["description"] = "Subscribe to view details."
                
            feed_plans.append(plan_data)
            
    return jsonify(feed_plans)

@app.route('/subscribe/<int:plan_id>', methods=['POST'])
@jwt_required()
def subscribe(plan_id):
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    plan = Plan.query.get(plan_id)
    
    if not plan:
        return jsonify({"message": "Plan not found"}), 404
        
    user.subscribed_plans.append(plan)
    db.session.commit()
    return jsonify({"message": "Subscribed successfully!"})

if __name__ == '__main__':
    app.run(debug=True)