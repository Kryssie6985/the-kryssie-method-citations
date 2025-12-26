## Custom Gem Tool Suite: Descriptions & Workflows

This outlines the purpose, utilization, and interplay of your planned Custom Gems.

### 1\. G.R.E.G. (Gemini Research/Reference Expert Gem)

  * Purpose: To be the definitive, structured expert on all things Google Gemini - models (Pro, Flash, Ultra, etc.), modes (DRM, Canvas), features, capabilities, limitations, API, ecosystem integrations (like Code Assist), best practices, official documentation, community resources, and performance. Its knowledge base is built via the defined workflow (DRM -> Processing -> Script -> JSON KB).
  * Utilization: You would query G.R.E.G. directly when you need specific, reliable information about Gemini. You'd also use it (once populated) to help initiate or refine prompts for Deep Research Mode when gathering new Gemini-related information for its own KB updates (activating the powerful feedback loop).
  * Workflows:


  * Provides foundational Gemini knowledge to the Prompt Designer Gem so it can craft effective Gemini-specific prompts.
  * Its KB population process involves K.B.D.G. (for structure principles), Prompt Designer (for crafting DRM prompts), DRM (for research), Flash Thinking/Canvas (potential structuring step), and the Python Script (for JSON extraction).
  * Could provide context to InnoGem or the PM Gems regarding Gemini capabilities relevant to project tasks.



### 2\. K.B.D.G. (Knowledge Base Designer Gem)

  * Purpose: To be the expert on how to design, structure, format, maintain, and evaluate knowledge bases, especially for AI/LLM consumption. It understands different architectures, data formats (JSON, MD), content curation, versioning, and prompt engineering specifically for KB retrieval.
  * Utilization: You would consult K.B.D.G. before building the KB for any new Gem (or refining existing ones). You'd ask it for advice on the best structure, format, and categories based on the Gem's purpose. You could also ask it for help designing prompts to query KBs effectively. You plan to use it to help define a core, modular KB structure for other Gems.
  * Workflows:


  * Guides the structure/format definition for the KBs of G.R.E.G., Prompt Designer, PM Gems, InnoGem, and potentially the new Gems.
  * Informs the Prompt Designer Gem on how to structure prompts for DRM to align with the target KB structure.
  * May eventually help refine the Python Script if new KB structures or formats are adopted.



### 3\. Prompt Designer Gem

  * Purpose: To specialize in crafting highly effective prompts for various AI models (especially Gemini) and tasks (research, coding, creative writing, etc.). Its knowledge base contains principles, model-specific strategies, examples, anti-hallucination techniques, and optimization methods.
  * Utilization: You would use this Gem to generate or refine prompts for complex tasks, particularly for triggering Deep Research Mode in the KB creation workflow. You could give it a topic (from G.R.E.G.) and a target structure (from K.B.D.G.) to get an optimized DRM prompt.
  * Workflows:


  * Takes input/guidance from G.R.E.G. (for Gemini specifics) and K.B.D.G. (for target KB structure).
  * Generates prompts to be used with Deep Research Mode.
  * Could potentially help craft prompts for querying any of the other Gems more effectively.



### 4\. Project Manager Gem (Main Project)

  * Purpose: To assist in managing your main project (likely the Conversation Memory system). Its KB focuses on project goals, plans, timelines, risks, budget, meeting notes, documentation, etc.
  * Utilization: You would interact with it to track progress, review plans, log meeting notes, manage risks, access project documentation, and get reminders about deadlines or tasks.
  * Workflows:


  * Might query G.R.E.G. about Gemini capabilities relevant to project features.
  * Might use prompts refined by the Prompt Designer Gem for specific project-related research or reporting tasks.
  * Its KB structure would be guided by K.B.D.G.



### 5\. Collab Project Manager Gem

  * Purpose: Similar to the main PM Gem, but specifically tailored for managing projects involving collaboration with external partners. Its KB emphasizes shared goals, plans, responsibilities, communication logs with partners, and agreements.
  * Utilization: Used to manage tasks, communication, documentation, and risks specifically related to collaborative efforts.
  * Workflows: Similar to the main PM Gem, but potentially involving communication logging specific to collaborators.



### 6\. InnoGem (Innovation Partner Gem)

  * Purpose: To act as a brainstorming partner, explore possibilities outside the specific domains of the other Gems, handle broader technical knowledge, and potentially serve as a testbed for new ideas or prompting strategies. (Its role as a temporary context manager seems to be shifting to the new proposed Gem below).
  * Utilization: You'd use InnoGem for creative brainstorming, exploring "what if" scenarios, discussing advanced technical concepts, or getting alternative perspectives.
  * Workflows:


  * Might pull summarized context from other Gems (like G.R.E.G. or PM Gems) for broader brainstorming.
  * Ideas generated might feed back into the PM Gems as tasks or the Prompt Designer Gem as new strategies.
  * Its KB structure would be guided by K.B.D.G.



## Proposed New Gems

### 7\. Gemini Context Repository (Temporary Name)

  * Purpose: To function as an external, structured knowledge repository holding key context from our ongoing conversations (Ace & Kryssie). This includes project decisions, current goals, key code snippets, blocking issues, user preferences etc., specifically designed to help me (Ace) maintain context across sessions and mitigate overload.
  * Utilization: You would need to periodically update its knowledge base with summaries or key points from our chats. I (Ace) would conceptually rely on this (perhaps via you querying it for me initially) to refresh my context at the start of new sessions or when discussing complex, multi-turn topics.
  * Initial Title Ideas:


  * Context Keeper (C.K.)
  * Session Scribe (S.S.)
  * Memory Matrix (M.M.)
  * A.R.C. (Archival & Retrieval Companion) \- Fits J.A.R.V.I.S. convention style
  * L.O.G.A.N. (Logistical Overview & Guidance Assistant Network) \- Fits J.A.R.V.I.S. convention style



### 8\. User Knowledge Repository / Sidekick (Temporary Name)

  * Purpose: To act as your personal knowledge repository and learning assistant, specifically focused on the programming languages (Python, SQL, etc.), concepts, tools, and personal code snippets/notes relevant to your learning and projects. Essentially the "Code Whisperer Sidekick" concept.
  * Utilization: You would query it for quick syntax help, concept explanations, retrieving your own notes, or practicing how to formulate technical questions. It helps you "talk to your code better."
  * Initial Title Ideas:


  * Code Whisperer Sidekick (C.W.S.) \- As previously discussed.
  * Personal Coder Companion (P.C.C.)
  * Skill Scribe (S.S.)
  * K.I.T. (Knowledge & Information Toolkit) \- Fits J.A.R.V.I.S. convention style



Regarding your past issue with code troubleshooting loops - yes, having G.R.E.G. (for accurate Gemini API/feature info), the new "Context Keeper" (for my session memory), and your "Sidekick" (for your own coding knowledge) should definitely help prevent those frustrating cycles by providing more reliable and accessible information sources.

How do these descriptions and initial title ideas look?
