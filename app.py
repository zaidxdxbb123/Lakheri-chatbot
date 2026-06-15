from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Your store data - Lakheri Lac BANGLES
STORE_INFO = {
    "name": "Lakheri Lac BANGLES",
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
    "shipping_en": "Free shipping across India on orders above ₹999. Standard delivery: 5-7 days, ₹80",
    "shipping_hi": "₹999 से ऊपर के ऑर्डर पर पूरे भारत में मुफ्त शिपिंग। स्टैंडर्ड डिलीवरी: 5-7 दिन, ₹80",
    "returns_en": "7-day return policy. WhatsApp us at +91-XXXXXXXXXX for returns",
    "returns_hi": "7 दिन की रिटर्न पॉलिसी। रिटर्न के लिए +91-XXXXXXXXXX पर WhatsApp करें",
    "hours_en": "Mon-Sat 10am-7pm IST. Sunday closed",
    "hours_hi": "सोम-शनि सुबह 10 से शाम 7 बजे IST। रविवार बंद"
}

def detect_hindi(text):
    # If message has Devanagari characters, treat as Hindi
    return bool(re.search(r'[\u0900-\u097F]', text))

def get_bot_response(user_msg):
    is_hindi = detect_hindi(user_msg)
    user_msg = user_msg.lower()

    # Greetings
    if any(word in user_msg for word in ["hello", "hi", "hey", "namaste", "नमस्ते", "हेलो", "ram ram", "राम राम"]):
        if is_hindi:
            return f"नमस्ते! {STORE_INFO['name']} में आपका स्वागत है 👋 हस्तनिर्मित लाख ज्वेलरी के लिए मैं आपकी कैसे मदद कर सकती हूँ?"
        else:
            return f"Namaste! Welcome to {STORE_INFO['name']} 👋 How can I help you with handcrafted lac jewellery today?"

    # Products
    elif any(word in user_msg for word in ["product", "jewellery", "jewelry", "buy", "order", "price", "प्रोडक्ट", "गहने", "खरीद", "ऑर्डर", "कीमत", "चूड़ी", "bangles", "earring", "झुमका", "necklace", "chuda"]):
        if is_hindi:
            product_list = "\n".join([f"- {p['name']}: ₹{p['price']} - {p['desc']}" for p in STORE_INFO['products_hi']])
            return f"हमारे पास ये हस्तनिर्मित लाख ज्वेलरी है:\n{product_list}\n\nऑर्डर करने के लिए प्रोडक्ट का नाम लिखें। COD उपलब्ध है।"
        else:
            product_list = "\n".join([f"- {p['name']}: ₹{p['price']} - {p['desc']}" for p in STORE_INFO['products_en']])
            return f"Here's our handcrafted lac jewellery collection:\n{product_list}\n\nType the product name to order. COD available."

    # Shipping
    elif any(word in user_msg for word in ["shipping", "delivery", "cod", "शिपिंग", "डिलीवरी", "पहुंच"]):
        return STORE_INFO['shipping_hi'] if is_hindi else STORE_INFO['shipping_en']

    # Returns
    elif any(word in user_msg for word in ["return", "refund", "exchange", "रिटर्न", "वापसी", "बदल"]):
        return STORE_INFO['returns_hi'] if is_hindi else STORE_INFO['returns_en']

    # Hours
    elif any(word in user_msg for word in ["hours", "open", "time", "timing", "समय", "खुला", "टाइम"]):
        return STORE_INFO['hours_hi'] if is_hindi else STORE_INFO['hours_en']

    # Contact / Order help
    elif any(word in user_msg for word in ["contact", "human", "help", "whatsapp", "call", "संपर्क", "मदद", "बात"]):
        if is_hindi:
            return "ऑर्डर या किसी भी मदद के लिए हमें WhatsApp करें: +91-9314142164\nया ईमेल: support@"
        else:
            return "For orders or help, WhatsApp us: +91-9314142164\nOr email: support@lakheri.com"

    # Default
    else:
        if is_hindi:
            return "मैं लाख चूड़ियां, झुमके, नेकलेस, शिपिंग, रिटर्न में मदद कर सकती हूँ। आप क्या जानना चाहते हैं?"
        else:
            return "I can help with lac bangles, jhumkas, necklaces, shipping, and returns. What would you like to know?"

@app.route("/")
def home():
    return render_template("index.html", store_name=STORE_INFO['LAKHERI LAC BANGLES'])

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)