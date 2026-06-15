from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

STORE_INFO = {
    "name": "Lakheri Lac Jewellery",
    "products_en": [
        {"id": 1, "name": "Lac Bangles Set", "price": 499, "desc": "Handcrafted Rajasthani lac bangles - Set of 6"},
        {"id": 2, "name": "Lac Jhumka Earrings", "price": 349, "desc": "Traditional lac work jhumkas with beads"},
        {"id": 3, "name": "Lac Pendant Necklace", "price": 599, "desc": "Colorful lac pendant with cotton dori"},
        {"id": 4, "name": "Lac Ring", "price": 199, "desc": "Adjustable lac ring with mirror work"},
        {"id": 5, "name": "Bridal Lac Chuda", "price": 1299, "desc": "Full set traditional bridal chuda"}
    ],
    "products_hi": [
        {"id": 1, "name": "लाख चूड़ी सेट", "price": 499, "desc": "हाथ से बनी राजस्थानी लाख चूड़ियां - 6 का सेट"},
        {"id": 2, "name": "लाख झुमका", "price": 349, "desc": "मोतियों के साथ पारंपरिक लाख झुमके"},
        {"id": 3, "name": "लाख पेंडेंट नेकलेस", "price": 599, "desc": "कॉटन डोरी के साथ रंगीन लाख पेंडेंट"},
        {"id": 4, "name": "लाख अंगूठी", "price": 199, "desc": "शीशे के काम वाली एडजस्टेबल लाख अंगूठी"},
        {"id": 5, "name": "ब्राइडल लाख चूड़ा", "price": 1299, "desc": "पूरा सेट पारंपरिक ब्राइडल चूड़ा"}
    ],
    "shipping_en": "Free shipping across India on orders above ₹999. Standard: 5-7 days, ₹80. COD available.",
    "shipping_hi": "₹999 से ऊपर के ऑर्डर पर पूरे भारत में मुफ्त शिपिंग। स्टैंडर्ड: 5-7 दिन, ₹80. COD उपलब्ध।",
    "returns_en": "7-day return policy. WhatsApp us: +91-9876543210",
    "returns_hi": "7 दिन की रिटर्न पॉलिसी। WhatsApp करें: +91-9876543210"
}

def detect_hindi(text):
    return bool(re.search(r'[\u0900-\u097F]', text))

def get_bot_response(user_msg):
    is_hindi = detect_hindi(user_msg)
    user_msg = user_msg.lower()
    
    if any(word in user_msg for word in ["hello", "hi", "namaste", "नमस्ते", "hey"]):
        return f"नमस्ते! {STORE_INFO['name']} में आपका स्वागत है 👋 मैं कैसे मदद कर सकती हूं?" if is_hindi else f"Namaste! Welcome to {STORE_INFO['name']} 👋 How can I help you?"
    
    elif any(word in user_msg for word in ["product", "price", "प्रोडक्ट", "कीमत", "chuda", "bangles", "jhumka", "ring", "चूड़ी", "झुमका"]):
        products = STORE_INFO['products_hi'] if is_hindi else STORE_INFO['products_en']
        product_list = "\n".join([f"- {p['name']}: ₹{p['price']}" for p in products])
        return f"हमारे प्रोडक्ट्स:\n{product_list}\n\nऑर्डर करने के लिए प्रोडक्ट का नाम भेजें।" if is_hindi else f"Our products:\n{product_list}\n\nSend product name to order."
    
    elif any(word in user_msg for word in ["shipping", "delivery", "cod", "शिपिंग", "डिलीवरी"]):
        return STORE_INFO['shipping_hi'] if is_hindi else STORE_INFO['shipping_en']
    
    elif any(word in user_msg for word in ["return", "exchange", "रिटर्न", "वापस"]):
        return STORE_INFO['returns_hi'] if is_hindi else STORE_INFO['returns_en']
    
    else:
        return "मैं चूड़ियां, झुमके, शिपिंग, रिटर्न में मदद कर सकती हूँ। आप क्या जानना चाहेंगे?" if is_hindi else "I can help with bangles, jhumkas, shipping, returns. What would you like to know?"

@app.route("/")
def home():
    return render_template("index.html", store_name=STORE_INFO['name'])

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)

