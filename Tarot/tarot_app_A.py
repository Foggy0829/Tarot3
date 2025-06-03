import streamlit as st
import random
import base64
import os
from PIL import Image
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Set up the page
st.set_page_config(
    page_title="Tarot Wisdom",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Custom CSS styling
st.markdown("""
<style>
    body {
        background-color: #e6e6fa;  /* 浅紫色 */
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        background: #e6e6fa;  /* 浅紫色 */
    }
</style>
""", unsafe_allow_html=True)
# Tarot deck data (Major Arcana only)
tarot_deck = [
    {
        "name": "The Fool",
        "image":"the_fool.jpg",
        "meaning_up": "New beginnings, innocence, spontaneity, a free spirit",
        "meaning_rev": "Recklessness, risk-taking, poor judgment, naivety",
        "description": "The Fool represents new beginnings, having faith in the future, being inexperienced, not knowing what to expect, having beginner's luck, improvisation and believing in the universe."
    },
    {
        "name": "The Magician",
        "image": "the_magician.jpg",
        "meaning_up": "Manifestation, resourcefulness, inspired action",
        "meaning_rev": "Manipulation, untapped talents, trickery",
        "description": "The Magician is the card of manifestation. When this card appears, it indicates that your visions are becoming reality. You have all the tools and resources you need to manifest your desires into being."
    },
    {
        "name": "The High Priestess",
        "image": "the_high_priestess.jpg",
        "meaning_up": "Intuition, unconscious knowledge, divine feminine",
        "meaning_rev": "Secrets, disconnected from intuition, withdrawal",
        "description": "The High Priestess is a symbol of hidden knowledge and intuition. She represents the subconscious mind and the divine feminine, encouraging you to trust your intuition and look beyond the obvious."
    },
    {
        "name": "The Empress",
        "image": "the_empress.jpg",
        "meaning_up": "Femininity, beauty, nature, abundance",
        "meaning_rev": "Creative block, dependence, overbearing",
        "description": "The Empress is the archetype of feminine power, creativity, and abundance. She represents nurturing, fertility, and the beauty of the natural world, encouraging you to embrace your sensuality and creative energy."
    },
    {
        "name": "The Emperor",
        "image": "the_emperor.jpg",
        "meaning_up": "Authority, structure, control, fatherhood",
        "meaning_rev": "Domination, rigidity, excessive control",
        "description": "The Emperor represents authority, structure, and leadership. He is a symbol of power and stability, encouraging you to take control of your life and establish order through logical thinking and planning."
    },
    {
        "name": "The Hierophant",
        "image": "the_hierophant.jpg",
        "meaning_up": "Tradition, spiritual wisdom, conformity",
        "meaning_rev": "Rebellion, challenging the status quo, new approaches",
        "description": "The Hierophant represents tradition, spiritual guidance, and conformity to social structures. This card encourages you to seek wisdom from established institutions or mentors and honor traditional values."
    },
    {
        "name": "The Lovers",
        "image": "the_lovers.jpg",
        "meaning_up": "Love, harmony, relationships, choices",
        "meaning_rev": "Imbalance, misalignment, disharmony",
        "description": "The Lovers card represents relationships, choices, and alignment. It often signifies an important decision regarding an existing relationship, a moral dilemma, or the choice between love and desire."
    },
    {
        "name": "The Chariot",
        "image": "the_chariot.jpg",
        "meaning_up": "Control, willpower, victory, assertion",
        "meaning_rev": "Lack of direction, aggression, force",
        "description": "The Chariot represents determination, willpower, and victory. This card signifies that through focus, discipline, and action, you will overcome obstacles and achieve your goals."
    },
    {
        "name": "Strength",
        "image": "strength.jpg",
        "meaning_up": "Courage, persuasion, influence, compassion",
        "meaning_rev": "Self-doubt, weakness, inner force",
        "description": "Strength represents courage, inner strength, and compassion. This card suggests that you have the ability to overcome challenges through inner fortitude and gentle persuasion rather than force."
    },
    {
        "name": "The Hermit",
        "image": "the_hermit.jpg",
        "meaning_up": "Soul-searching, introspection, inner guidance",
        "meaning_rev": "Isolation, loneliness, withdrawal",
        "description": "The Hermit represents introspection, soul-searching, and inner guidance. This card suggests a time for self-reflection, seeking wisdom within, and withdrawing from the outside world to find answers."
    },
    {
        "name": "Wheel of Fortune",
        "image": "wheel_of_fortune.jpg",
        "meaning_up": "Destiny, turning point, cycles, fate",
        "meaning_rev": "Bad luck, resistance to change, lack of control",
        "description": "The Wheel of Fortune represents destiny, turning points, and the cycles of life. This card signifies that change is coming, and you must be ready to adapt to the turning of fate's wheel."
    },
    {
        "name": "Justice",
        "image": "justice.jpg",
        "meaning_up": "Fairness, truth, cause and effect",
        "meaning_rev": "Injustice, dishonesty, unfairness",
        "description": "Justice represents fairness, truth, and the law of cause and effect. This card suggests that balance will be restored, and you will be held accountable for your actions."
    },
    {
        "name": "The Hanged Man",
        "image": "the_hanged_man.jpg",
        "meaning_up": "Surrender, new perspective, suspension",
        "meaning_rev": "Stalling, resistance, avoiding sacrifice",
        "description": "The Hanged Man represents surrender, new perspectives, and suspension. This card suggests that by letting go and looking at things differently, you will gain valuable insights."
    },
    {
        "name": "Death",
        "image": "death.jpg",
        "meaning_up": "Endings, change, transformation",
        "meaning_rev": "Resistance to change, stagnation, fear",
        "description": "Death represents endings, transformation, and change. This card signifies that something in your life is coming to an end, making way for new beginnings and transformation."
    },
    {
        "name": "Temperance",
        "image": "temperance.jpg",
        "meaning_up": "Balance, moderation, purpose, healing",
        "meaning_rev": "Imbalance, excess, lack of purpose",
        "description": "Temperance represents balance, moderation, and purpose. This card suggests finding the middle path, practicing patience, and integrating different aspects of your life to create harmony."
    },
    {
        "name": "The Devil",
        "image": "the_devil.jpg",
        "meaning_up": "Shadow self, bondage, materialism",
        "meaning_rev": "Releasing limiting beliefs, freedom, reclaiming power",
        "description": "The Devil represents the shadow self, bondage, and materialism. This card suggests that you may be trapped by limiting beliefs, addictions, or unhealthy attachments that are preventing your growth."
    },
    {
        "name": "The Tower",
        "image": "the_tower.jpg",
        "meaning_up": "Sudden change, revelation, awakening",
        "meaning_rev": "Avoiding disaster, resisting change, fear",
        "description": "The Tower represents sudden change, revelation, and awakening. This card signifies that a dramatic upheaval may occur, shattering existing structures but ultimately leading to liberation and truth."
    },
    {
        "name": "The Star",
        "image": "the_star.jpg",
        "meaning_up": "Hope, faith, purpose, renewal",
        "meaning_rev": "Hopelessness, despair, lack of faith",
        "description": "The Star represents hope, faith, and renewal. This card brings a message of inspiration, healing, and spiritual guidance, suggesting that you should maintain faith in the universe."
    },
    {
        "name": "The Moon",
        "image": "the_moon.jpg",
        "meaning_up": "Illusion, intuition, unconscious, anxiety",
        "meaning_rev": "Releasing fear, repressed emotion, confusion",
        "description": "The Moon represents illusion, intuition, and the unconscious. This card suggests that things are not as they seem, and you may need to explore your deeper emotions and intuitive insights."
    },
    {
        "name": "The Sun",
        "image": "the_sun.jpg",
        "meaning_up": "Positivity, success, vitality, joy",
        "meaning_rev": "Temporary depression, lack of success, pessimism",
        "description": "The Sun represents positivity, success, and joy. This card brings warmth, happiness, and success, indicating that you are entering a period of abundance and vitality."
    },
    {
        "name": "Judgement",
        "image": "judgement.jpg",
        "meaning_up": "Reflection, reckoning, inner calling",
        "meaning_rev": "Self-doubt, refusal of the call, fear",
        "description": "Judgement represents reflection, reckoning, and inner calling. This card suggests a time of self-evaluation, awakening, and heeding a higher calling to fulfill your life's purpose."
    },
    {
        "name": "The World",
        "image": "the_world.jpg",
        "meaning_up": "Completion, integration, accomplishment",
        "meaning_rev": "Lack of closure, unfinished business, stagnation",
        "description": "The World represents completion, integration, and accomplishment. This card signifies the successful conclusion of a cycle, achievement of goals, and a sense of wholeness and fulfillment."
    }
]

# 获取卡片图像的函数
def get_card_image(card_data, orientation):
    """获取卡片图像，处理正逆位"""
    try:
        # 获取图片文件名
        image_file = card_data["image"]
        
        # 创建图片路径
        image_path = os.path.join("images", image_file)
        
        # 检查图片是否存在
        if os.path.exists(image_path):
            # 打开图片
            img = Image.open(image_path)
            
            # 如果是逆位，旋转图片
            if orientation == "reversed":
                img = img.rotate(180)
                
            return img
        else:
            # 如果图片不存在，生成占位符
            st.warning(f"Image not found: {image_path}")
            return generate_card_svg(card_data["name"], orientation == "reversed")
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return generate_card_svg(card_data["name"], orientation == "reversed")

# Function to generate a placeholder card image with SVG
def generate_card_svg(card_name, reversed=False, width=200, height=350):
    """Generate SVG placeholder card"""
    
    # Define gradient colors
    color1 = "#9370DB"  # Medium Purple
    color2 = "#483D8B"  # Dark Slate Blue
    
    # Rotate text if card is reversed
    text_transform = f'transform="rotate(180,{width//2},{height//2})"' if reversed else ""
    
    svg = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{color1}" />
                <stop offset="100%" stop-color="{color2}" />
            </linearGradient>
        </defs>
        <rect width="{width-10}" height="{height-10}" x="5" y="5" rx="15" ry="15" fill="url(#grad)" stroke="#f1f1f1" stroke-width="2" />
        <rect width="{width-30}" height="{height-30}" x="15" y="15" rx="10" ry="10" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.3)" stroke-width="1" />
        <text x="{width//2}" y="{height//2}" font-family="Arial" font-size="14" fill="white" text-anchor="middle" font-weight="bold" {text_transform}>{card_name}</text>
    </svg>
    """
    
    # Encode SVG to base64
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"
# App title and header
st.markdown("<h1 style='color: #813399;'>🔮 Tarot Wisdom</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #813399;'>Explore your past, present, and future with ancient wisdom</h3>", unsafe_allow_html=True)

# User question input
with st.expander("You may ask some questions to get started."):
    st.markdown("<p style='color: black; font-size: 20px;'>Concentrate on your question before drawing cards</p>", unsafe_allow_html=True)
    user_question = st.text_area("",
                               placeholder="Example: What do I need to know about my career path? How will my relationship develop?")

# Draw cards button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Create a gradient background style for the button
    button_style = """
        <style>
            div.stButton > button {
                background: linear-gradient(135deg, #9370DB, #483D8B);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            div.stButton > button:hover {
                background: linear-gradient(135deg, #483D8B, #9370DB);
            }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    draw_button = st.button("✨ Draw Tarot Cards", use_container_width=True)

# Initialize session state for cards
if 'cards_drawn' not in st.session_state:
    st.session_state.cards_drawn = False
    st.session_state.past_card = None
    st.session_state.present_card = None
    st.session_state.future_card = None
    st.session_state.past_orientation = "upright"
    st.session_state.present_orientation = "upright"
    st.session_state.future_orientation = "upright"

# Draw cards when button is clicked
if draw_button:
    st.session_state.cards_drawn = True
    # Randomly select three distinct cards
    selected_cards = random.sample(tarot_deck, 3)
    st.session_state.past_card = selected_cards[0]
    st.session_state.present_card = selected_cards[1]
    st.session_state.future_card = selected_cards[2]
    
    # Randomly determine orientation for each card
    st.session_state.past_orientation = random.choice(["upright", "reversed"])
    st.session_state.present_orientation = random.choice(["upright", "reversed"])
    st.session_state.future_orientation = random.choice(["upright", "reversed"])
    
    # Animation effect
    st.balloons()

# 显示卡片（如果已抽取）
if st.session_state.cards_drawn:
    st.success("Your cards have been drawn! Here is your reading:")
    
    # 为三张牌创建列
    col1, col2, col3 = st.columns(3)
    
    # 过去牌
    with col1:
        st.markdown("<h3 style='color: #813399;'>Past</h3>", unsafe_allow_html=True)
        st.markdown(f"**{st.session_state.past_card['name']}**")
        st.markdown(f"*({st.session_state.past_orientation.capitalize()})*")
        
        # 获取卡片图像
        card_img = get_card_image(
            st.session_state.past_card, 
            st.session_state.past_orientation
        )
        
        # 显示卡片图像
        if isinstance(card_img, Image.Image):  # 如果是PIL图像
            st.image(card_img, use_container_width=True, 
                    caption=f"{st.session_state.past_card['name']} ({st.session_state.past_orientation})")
        else:  # 如果是SVG字符串
            st.image(card_img, use_container_width=True, 
                    caption=f"{st.session_state.past_card['name']} ({st.session_state.past_orientation})")
        
        # 卡片含义
        if st.session_state.past_orientation == "upright":
            meaning = st.session_state.past_card['meaning_up']
        else:
            meaning = st.session_state.past_card['meaning_rev']
        st.info(f"**Meaning:** {meaning}")
        
        # 卡片描述
        with st.expander("Card Interpretation"):
            st.write(st.session_state.past_card['description'])
    
    # 现在牌
    with col2:
        st.markdown("<h3 style='color: #813399;'>Present</h3>", unsafe_allow_html=True)
        st.markdown(f"**{st.session_state.present_card['name']}**")
        st.markdown(f"*({st.session_state.present_orientation.capitalize()})*")
        
        # 获取卡片图像
        card_img = get_card_image(
            st.session_state.present_card, 
            st.session_state.present_orientation
        )
        
        # 显示卡片图像
        if isinstance(card_img, Image.Image):  # 如果是PIL图像
            st.image(card_img, use_container_width=True, 
                    caption=f"{st.session_state.present_card['name']} ({st.session_state.present_orientation})")
        else:  # 如果是SVG字符串
            st.image(card_img, use_container_width=True, 
                    caption=f"{st.session_state.present_card['name']} ({st.session_state.present_orientation})")
        
        # 卡片含义
        if st.session_state.present_orientation == "upright":
            meaning = st.session_state.present_card['meaning_up']
        else:
            meaning = st.session_state.present_card['meaning_rev']
        st.info(f"**Meaning:** {meaning}")
        
        # 卡片描述
        with st.expander("Card Interpretation"):
            st.write(st.session_state.present_card['description'])
    
    # 未来牌
    with col3:
        st.markdown("<h3 style='color: #813399;'>Future</h3>", unsafe_allow_html=True)
        st.markdown(f"**{st.session_state.future_card['name']}**")
        st.markdown(f"*({st.session_state.future_orientation.capitalize()})*")
        
        # 获取卡片图像
        card_img = get_card_image(
            st.session_state.future_card, 
            st.session_state.future_orientation
        )
        
        # 显示卡片图像
        if isinstance(card_img, Image.Image):  # 如果是PIL图像
            st.image(card_img, use_container_width=True, 
                    caption=f"{st.session_state.future_card['name']} ({st.session_state.future_orientation})")
        else:  # 如果是SVG字符串
            st.image(card_img, use_container_width=True, 
                    caption=f"{st.session_state.future_card['name']} ({st.session_state.future_orientation})")
        
        # 卡片含义
        if st.session_state.future_orientation == "upright":
            meaning = st.session_state.future_card['meaning_up']
        else:
            meaning = st.session_state.future_card['meaning_rev']
        st.info(f"**Meaning:** {meaning}")
        
        # 卡片描述
        with st.expander("Card Interpretation"):
            st.write(st.session_state.future_card['description'])
    
    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Overall reading interpretation
    st.markdown("<h3 style='color: #813399;'>Overall Reading</h3>", unsafe_allow_html=True)
    
    # Get the appropriate meaning based on orientation
    past_meaning = st.session_state.past_card['meaning_rev'].lower() if st.session_state.past_orientation == "reversed" else st.session_state.past_card['meaning_up'].lower()
    present_meaning = st.session_state.present_card['meaning_rev'].lower() if st.session_state.present_orientation == "reversed" else st.session_state.present_card['meaning_up'].lower()
    future_meaning = st.session_state.future_card['meaning_rev'].lower() if st.session_state.future_orientation == "reversed" else st.session_state.future_card['meaning_up'].lower()
    
    interpretation = f"""
    <div class="reading-section" style="background-color: white; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <b>Past Influence:</b> The {st.session_state.past_card['name']} card in the {st.session_state.past_orientation} position suggests that {past_meaning} has played a significant role in shaping your current situation.<br><br><b>Present Situation:</b> The {st.session_state.present_card['name']} card in the {st.session_state.present_orientation} position suggests that {present_meaning} has played a significant role in your life right now.<br><br><b>Future Potential:</b> The {st.session_state.future_card['name']} card in the {st.session_state.future_orientation} position suggests that {future_meaning} could influence your upcoming experiences.<br><br><b>Guidance:</b> The cards suggest reflecting on your past experiences and considering how they shape your current path.
    </div>
    """
    st.markdown(interpretation, unsafe_allow_html=True)
    
    # Advice section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #813399;'>Advice from the Cards</h3>", unsafe_allow_html=True)
    advice = """
    <div class="reading-section" style="background-color: white; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <p style="color: black;">1. <b>Reflect on the past:</b> Consider how previous experiences have shaped your current situation. What lessons can you take forward?</p>
        <p style="color: black;">2. <b>Embrace the present:</b> Focus on what you can control right now. How can you align your actions with your highest good?</p>
        <p style="color: black;">3. <b>Shape your future:</b> The future card shows potential outcomes, not fixed destiny. What steps can you take to manifest the best possible future?</p>
        <p style="color: black;">4. <b>Trust your intuition:</b> Tarot reveals possibilities, but you have the wisdom within to make the right choices.</p>
    </div>
    """
    st.markdown(advice, unsafe_allow_html=True)

# Sidebar information
st.sidebar.header("About Tarot Wisdom")
st.sidebar.image("images/sidephoto.jpg", use_container_width=True)
st.sidebar.write("""
This three-card Tarot reading offers insight into:

- **Past:** Influences that have shaped your current situation
- **Present:** Your current circumstances and challenges
- **Future:** Potential outcomes based on current energies

Tarot cards serve as a mirror to your subconscious, helping you gain clarity and perspective.
""")

st.sidebar.divider()

st.sidebar.header("How to Use")
st.sidebar.write("""
1. Focus on a question or area of your life
2. Click "Draw Tarot Cards" when you feel ready
3. Reflect on each card's meaning in its position
4. Consider how the overall reading applies to your situation
5. Use the insights for personal reflection
""")

st.sidebar.divider()

st.sidebar.header("Important Notes")
st.sidebar.info("""
- Tarot readings are for guidance only
- You have free will to shape your future
- Readings reflect current energies which can change
- Consult professionals for important decisions
- This is not a substitute for professional advice
""")

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: white;">Tarot Wisdom &copy; 2025 | This application is for entertainment purposes only</p>
        <p style="color: white;">The interpretations are based on traditional Tarot symbolism</p>
    </div>
</div>
""", unsafe_allow_html=True)

