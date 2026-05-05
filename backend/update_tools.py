import json
import os

tools_path = r'd:\Avinash\Rect\ai-all-in-one\backend\tools.json'
with open(tools_path, 'r') as f:
    tools = json.load(f)

new_tools_raw = """Perplexity AI, YouChat, Poe AI, DeepSeek AI, Microsoft Copilot, Google AI Studio, HuggingChat, Pi AI, Sudowrite, Wordtune, HyperWrite, Peppertype AI, Anyword, Ink AI, LongShot AI, Simplified Writer, TextCortex, Katteb, ClosersCopy, Sapling AI, NovelCrafter, AISEO, WriterZen, ProWritingAid AI, Linguix, Rephrase AI, Typli AI, Hoppy Copy, Smart Copy, NeuralText, Stable Diffusion, BlueWillow, NightCafe, Fotor AI, PhotoRoom, Remini, Cutout Pro, Artbreeder, StarryAI, Deep Dream Generator, Imagine AI, Picsart AI, Designs.ai, Hotpot AI, Krea AI, Magnific AI, Pixelcut, FaceApp AI, ZMO AI, VanceAI, Kaiber AI, Wisecut, Colossyan, Elai.io, Hour One, Vidyo AI, Kapwing AI, Filmora AI, Opus Clip, Descript Studio, Unscreen, Steve AI, Raw Shorts, Promo AI, Animaker AI, Powtoon AI, Dubverse, Synthesys AI, Wave.video AI, FlexClip AI, Continue AI, Sourcegraph Cody, Bolt.new, Windsurf AI, Phind AI, CodeGeeX, Pieces AI, Safurai, Mintlify AI, Bito AI, Tabby AI, Codiumate, DeepCode AI, Qodo AI, JetBrains AI Assistant, Devin AI, Aider AI, Smol Developer, Cursor Composer, AutoGPT, Suno AI, Udio, Voicemod AI, VocalRemover AI, Cleanvoice AI, Podcastle AI, Adobe Podcast AI, Listnr AI, WellSaid Labs, TTSMaker, Browse AI, Akkio, Obviously AI, MonkeyLearn, DataRobot, Teachable Machine, Levity AI, Peltarion, BigML, ObviouslyML, Durable Website Builder, 10Web AI Builder, Framer AI, Wix ADI, Hostinger AI Builder, Jimdo Dolphin, B12 AI, Bookmark AiDA, Unicorn Platform AI, Zyro AI, Tome App, Decktopus AI, SlidesAI, Presentations.ai, Pitch AI, Canva Magic Design, Gamma App, Beautiful Slides AI, Sendsteps AI, PopAi, Krisp, Fireflies, Fathom AI, Avoma, tl;dv AI, Grain AI, Sembly AI, Supernormal, MeetGeek, Fellow AI, Motion, Reclaim AI, Clockwise AI, Trevor AI, BeforeSunset AI, Taskade, Notion Q&A, Mem X, ClickUp Brain, Asana Intelligence, Midpage AI, Glean AI, Humata AI, ChatPDF, AskYourPDF, SciSpace Copilot, Elicit AI, Consensus AI, Explainpaper, Scholarcy, Jasper Art, LogoAI, Looka, Brandmark, Tailor Brands AI, Khroma, Uizard, Galileo AI, Visily AI, Mockey AI, Replit Ghostwriter, Hex Magic AI, Rows AI, Airtable AI, Coda AI, Zapier AI, Make AI, Pabbly AI, n8n AI, Bardeen AI, Tidio AI, Intercom Fin, Zendesk AI, Freshdesk Freddy AI, Drift AI, ManyChat AI, Chatfuel AI, Kommunicate AI, Botpress AI, Landbot AI, AdCreative, Predis, Ocoya, CopySmith, Smartly.io AI, Pencil AI, Phrasee, Pattern89, Madgicx AI, Albert AI, Surfer AI, Frase.io, WriterSonic SEO, Outranking, GrowthBar, Diib AI, Alli AI SEO, Page Optimizer Pro AI, RankIQ, Seobility AI, Resume.io AI, Kickresume AI, Rezi AI, Teal AI, Huntr AI, Jobscan AI, Careerflow AI, Interview Warmup AI, Final Round AI, Yoodli AI, DoNotPay AI, Casetext CoCounsel, Harvey AI, Spellbook AI, Lexis+ AI, EvenUp AI, Luminance AI, Ebrevia AI, Klarity AI, Robin AI, Ada Health AI, K Health, Med-PaLM, Glass Health, Symptomate, Buoy Health, Abridge AI, Nabla Copilot, Suki AI, PathAI, Socratic AI, Khanmigo, Quizlet Q-Chat, TutorAI, Duolingo Max, Elsa Speak AI, Photomath AI, Brainly AI, Course Hero AI, Studocu AI, Character Creator AI, Inworld AI, Scenario AI, Rosebud AI, Leonardo Motion, Meshy AI, Luma AI, Spline AI, Wonder Dynamics, Cascadeur AI, Replica Studios, Altered Studio, Voiceflow AI, Synthflow AI, Retell AI, Vapi AI, Bland AI, Air.ai, PolyAI, Cognigy AI, Mixo AI, Namelix, ValidatorAI, IdeaBuddy AI, Bizway AI, Upmetrics AI, LivePlan AI, Venturekit AI, FounderPal AI, Brand24 AI, Cleanup.pictures, Let’s Enhance, ImgUpscaler AI, Nero AI Image Upscaler, Topaz Photo AI, Topaz Video AI, HitPaw AI, iLoveIMG AI, Remove.bg, Clipdrop, PromptHero, FlowGPT, Snack Prompt, PromptBase, AIPRM, PromptPerfect, PromptLayer, LangChain, LlamaIndex, CrewAI"""

names = [n.strip() for n in new_tools_raw.split(',') if n.strip()]

cat_map = {
    'Text': ['Perplexity', 'YouChat', 'Poe', 'DeepSeek', 'Copilot', 'Pi', 'Sudowrite', 'Wordtune', 'HyperWrite', 'Anyword', 'Writer', 'Text', 'Novel', 'Linguix', 'Rephrase', 'Hoppy', 'Neural'],
    'Image': ['Diffusion', 'BlueWillow', 'NightCafe', 'Fotor', 'Artbreeder', 'Imagine', 'Picsart', 'Designs', 'Hotpot', 'Krea', 'Magnific', 'Pixelcut', 'FaceApp', 'ZMO', 'Cleanup', 'Enhance', 'Upscaler'],
    'Video': ['Kaiber', 'Wisecut', 'Colossyan', 'Elai', 'Hour One', 'Vidyo', 'Kapwing', 'Filmora', 'Opus', 'Descript', 'Unscreen', 'Steve', 'Raw', 'Promo', 'Animaker', 'Powtoon', 'Dubverse', 'FlexClip', 'Wonder', 'Cascadeur'],
    'Coding': ['Cody', 'Bolt', 'Windsurf', 'Phind', 'Code', 'Pieces', 'Safurai', 'Mintlify', 'Bito', 'Tabby', 'Codiumate', 'DeepCode', 'Qodo', 'Devin', 'Aider', 'Smol', 'Cursor', 'AutoGPT', 'Replit', 'LangChain', 'LlamaIndex', 'CrewAI'],
    'Voice': ['Suno', 'Udio', 'Voicemod', 'Vocal', 'Cleanvoice', 'Podcastle', 'Listnr', 'WellSaid', 'TTS', 'Replica Studios', 'Altered', 'Voiceflow', 'Vapi', 'Bland', 'Air', 'Poly'],
    'Productivity': ['Krisp', 'Fireflies', 'Fathom', 'Avoma', 'Grain', 'Sembly', 'Supernormal', 'MeetGeek', 'Fellow', 'Motion', 'Reclaim', 'Clockwise', 'Trevor', 'Taskade', 'Notion', 'Mem', 'ClickUp', 'Asana', 'Humata', 'ChatPDF', 'AskYourPDF', 'SciSpace', 'Elicit', 'Consensus', 'Scholarcy'],
    'Business': ['Durable', '10Web', 'Framer', 'Wix', 'Hostinger', 'Jimdo', 'B12', 'Bookmark', 'Unicorn', 'Zyro', 'Tome', 'Decktopus', 'Slides', 'Pitch', 'Canva', 'Gamma', 'Beautiful', 'Zapier', 'Make', 'n8n', 'Tidio', 'Intercom', 'Zendesk', 'Botpress', 'AdCreative', 'Ocoya', 'Mixo', 'IdeaBuddy', 'Bizway', 'Venturekit', 'FounderPal'],
    'SEO': ['Surfer', 'Frase', 'RankIQ', 'WriterZen', 'Seobility', 'Page Optimizer', 'RankIQ', 'Alli AI', 'Outranking', 'GrowthBar'],
    'Fun': ['Character', 'Inworld', 'Scenario', 'Rosebud', 'Luma', 'Spline']
}

for name in names:
    if any(t['name'] == name for t in tools): continue
    category = 'text'
    for k, v in cat_map.items():
        if any(word.lower() in name.lower() for word in v):
            category = k.lower()
            break
    
    tools.append({
        'name': name,
        'category': category,
        'tag': category.upper() + ' AI',
        'desc': f'Advanced {category} tools powered by AI to enhance your workflow and creativity.',
        'link': 'https://google.com/search?q=' + name.replace(' ', '+'),
        'img': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=400'
    })

with open(tools_path, 'w') as f:
    json.dump(tools, f, indent=4)
print(f'Done! Total tools: {len(tools)}')
