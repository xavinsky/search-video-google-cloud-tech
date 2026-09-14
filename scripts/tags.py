"""Taxonomie des tags, regroupés par famille technologique.

Chaque vidéo reçoit tous les tags dont la regex matche son titre (insensible à la casse) —
une vidéo peut donc porter plusieurs tags, dans plusieurs familles.

Règle : aucun tag fourre-tout ("Autres", "Divers"...). Une vidéo qui ne matche rien est listée
par build.py pour qu'on lui trouve un tag précis — via une regex dans GROUPS si le sujet est
récurrent, via MANUAL_OVERRIDES si le titre est un cas isolé.
"""

GROUPS = [
    ("Data & Analytics", [
        ("BigQuery", r"bigquery|big query|biglake|user-defined function|running queries|query results|asking questions|google cloud data analytics"),
        ("BigQuery ML", r"bigquery ml"),
        ("Dataflow / Apache Beam", r"dataflow|apache beam|\bbeam\b"),
        ("Pub/Sub", r"pub/?sub"),
        ("Dataproc / Spark", r"dataproc|apache spark"),
        ("Dataplex / Data Catalog", r"dataplex|knowledge catalog|data catalog|data governance|data mesh"),
        ("Analytics Hub / Data Sharing", r"analytics hub|data shar|data exchange"),
        ("Composer / Airflow", r"cloud composer|apache airflow"),
        ("Data Fusion / Dataprep", r"data fusion|dataprep|trifacta"),
        ("Datastream / CDC", r"datastream"),
        ("Kafka / Streaming", r"apache kafka|\bkafka\b"),
        ("Looker / Looker Studio", r"\blooker\b|lookml|data studio"),
    ]),
    ("Bases de données", [
        ("Cloud Spanner", r"\bspanner\b"),
        ("AlloyDB", r"alloydb"),
        ("Cloud SQL", r"cloud sql|cloudsql"),
        ("Firestore", r"firestore"),
        ("Bigtable", r"bigtable"),
        ("Memorystore", r"memorystore"),
        ("Migration de bases de données", r"database migration service|harbourbridge|oracle|sql server"),
        ("Graph databases (Neo4j)", r"neo4j|graph database|graph engineering"),
        ("PostgreSQL / MySQL", r"postgresql|\bmysql\b"),
        ("Bases de données : concepts", r"nosql|\bsql\b managed|choose the right.*database|database (deployment|configuration|center)|golden demo|databases?\b|data warehouse"),
    ]),
    ("IA & Machine Learning", [
        ("Vertex AI", r"vertex ai"),
        ("Gemini / GenAI", r"\bgemini\b|generative ai|\brag\b|duet ai|\bgemma\b|retrieval augmented generation|\bgen ai\b|#genai|#generativeai|champion innovator|\bai\b"),
        ("Machine Learning (général)", r"machine learning|\bllms?\b|large language model|\bjax\b|tensorflow|pytorch|vllm|\binference\b|transformer|attention mechanism|embeddings?|federated learning|foundation models?|explainable ai|human-in-the-loop|neural network|deep learning|\bbert\b|automl|kubeflow|mlops|\btfx\b|classification model|model garden|semantic (search|modeling)|parameter efficient tuning|fine-tuning|training an? model|tuning .*model|predictions? from|model types|hugging face|\bfhir\b|healthcare api|\bt5\b|\bgpt\b|kfserving|natural language processing|custom training|\bpipelines?\b|transcribe|custom ml model|teach themselves|domain specific language model|digitize text"),
        ("Agents IA", r"\bagents?\b|agentic"),
        ("ADK / Multi-agent", r"\badk\b|agent development kit|multi-agent"),
        ("A2A", r"\ba2a\b"),
        ("MCP", r"model context protocol|\bmcp\b"),
        ("Patterns de conception agents", r"\bpattern\b"),
        ("Mémoire des agents", r"\bmemory\b"),
        ("Prompt Engineering", r"\bprompt"),
        ("AI Studio / Vibe Coding", r"ai studio|vibe coding|no-code|low-code"),
        ("Antigravity", r"antigravity"),
        ("Gemini CLI / Coding agents", r"gemini cli|coding agent|loop engineering|tokenmaxxing|imaxxing|/goal\b|developer plugin"),
        ("NotebookLM", r"notebooklm"),
        ("Imagen / Veo / Génération média", r"image generation|video generation|image editing|video editing|gen media|\bimagen\b|\bveo\b|nano banana|image captioning"),
        ("Speech-to-Text", r"speech-to-text"),
        ("Document AI", r"document ai"),
        ("Video Intelligence", r"video intelligence"),
        ("Natural Language API", r"natural language api"),
        ("Vision API", r"vision api"),
        ("Contact Center AI / Dialogflow", r"dialogflow|\bccai\b|contact center|ivr\b|conversational agent"),
        ("Colab", r"\bcolab\b"),
        ("DeepMind", r"deepmind"),
        ("Hardware IA (TPU / GPU)", r"\bhardware\b|\bchips?\b|\btpus?\b|axion processor|\bgpus?\b|hypercomputer|workload scheduler|dynamic workload"),
        ("IA : évaluation & tests", r"evaluat|\btesting\b|accuracy pipeline|ai app.{0,25}working|know my ai app"),
        ("IA : applications & chatbots", r"chat apps?|chatbot|\bai app\b|image search app|personal website|mobile ad platform|enterprise search|recommendations ai|ai assistant|social media photo|ecommerce platform|priority lane"),
        ("IA : cas d’usage sectoriels", r"healthcare|pregnan|wildfire|weather|climate|translat.*baby|billboard|\bmanga\b|agriculture|retail\b|moms in india|saving moms"),
        ("IA : adoption & stratégie", r"\badoption\b|platform strategy|business intelligence|enterprise ai|unlocking ai"),
    ]),
    ("Compute & Conteneurs", [
        ("Kubernetes / GKE", r"\bgke\b|kubernetes|\bcontainers?\b"),
        ("Cloud Run", r"cloud run"),
        ("Cloud Functions", r"cloud functions|private cloud function"),
        ("App Engine", r"app engine"),
        ("Compute Engine / VMs", r"compute engine|\bvms?\b|managed instance group|\bmig\b|virtual machine|canary updates|persistent runtimes|compute options|digits of pi|pi world record"),
        ("Serverless / Architecture", r"serverless|scalab|distributed (system|architecture)|\barchitecture\b|event-driven|event driven|\bfaas\b|stateful workloads"),
        ("Cluster Director / HPC", r"cluster director|high performance computing|\bhpc\b|\bbatch\b"),
        ("Cloud Workstations", r"cloud workstations?|#workstations"),
        ("VMware / GCVE", r"\bgcve\b|vmware"),
        ("Distributed Cloud / Multi-cloud", r"distributed cloud|hybrid.{0,20}multi-cloud|multi-cloud|hybrid environments"),
        ("Mainframe", r"mainframe"),
    ]),
    ("Stockage & Fiabilité", [
        ("Cloud Storage", r"cloud storage|\bstorage\b|filestore|persistent disk|local ssd"),
        ("Backup / Reliability / SRE", r"backup|disaster recovery|\bsre\b|reliabilit|sustained use|reliable systems"),
        ("Data centers / Infrastructure physique", r"data center|carbon|sustainab|satellites?|land cover maps|dynamic world|eda workload"),
    ]),
    ("Réseau", [
        ("Networking", r"\bnetwork(ing)?\b|\bvpc\b|load balanc|firewall|recaptcha|private google access|custom next hop|\bdns\b|interconnect|\bnat\b|private service connect|public ips?|\bcdn\b|\bedge\b|immersive stream|subsea cable|service mesh|edge computing|global front end|virtual private cloud"),
    ]),
    ("Sécurité & Identité", [
        ("Sécurité", r"security|zero trust|\bdlp\b|model armor|sensitive data protection|confidential|protect\w*|cyberattack|red teaming|threat detection|least privilege|authorized views|de-identif|cloud armor|\bwaf\b|\bngfw\b|secure web proxy|secops|\bkms\b|encrypt|mandiant|permission errors|attack path|risk scoring|redact|classify sensitive|secure (data|apps)|secure your cloud|responsible ai|securing web applications"),
        ("IAM / Identity / Policy", r"\biam\b|identity|policy intelligence|service accounts?|resource manager|policy troubleshooter|policy simulator|organization polic|custom roles|resource hierarchy|payments profile|org(anization)? restriction|custom org policy|app management.*folder"),
        ("Secret Manager", r"secret manager"),
        ("Certificate Authority Service", r"\bcas\b|certificate authority"),
        ("Assured Workloads / Conformité", r"assured workloads?|assured (open source|oss)|\bcompliance\b|\bcompliant\b|regulated (industr|organization)|sovereignty|criminal justice|fraud prevention|public sector|software supply chain|policy analyzer"),
        ("OS Login / SSH", r"os login|\bssh\b"),
        ("Chrome Enterprise", r"chrome (enterprise|browser)"),
    ]),
    ("DevOps & Opérations", [
        ("DevOps / CI-CD / IaC", r"cloud build|ci/cd|devops|terraform|cloud deploy|blue-green|canary|infrastructure as code|application design center"),
        ("Monitoring / Observability", r"monitoring|observability|prometheus|\bslos?\b|logging|opentelemetry|error reporting|alerting|log analytics|log sink|metadata management|magic quadrant|quotas?|cloud operations|ops agent|system insights|node not ready|distributed tracing|profiling"),
        ("Cloud Workflows / Eventarc", r"cloud workflows|\borchestration\b|choreography|eventarc|saga pattern|parallel steps"),
        ("Application Integration", r"application integration"),
        ("Cloud Tasks / Scheduler", r"cloud tasks|cloud scheduler|cron jobs?"),
        ("Active Assist", r"active assist|cloud assist"),
        ("Client Libraries / Dev Tools", r"client librar|cloud code|artifact registry|\bsdk\b|\bcli\b|gcloud command|cloud shell|code & build tools|platform overview"),
        ("Productivité développeur", r"\bproductivity\b|developer platform|platform engineering"),
        ("Frameworks, langages & outils de code", r"\bgo\b (application|1\.18)|spring (boot|native)|\bangular\b|react app|vue\.?js|java (producer|spring)|\.net\b|\bwebsite\b|e-?commerce|\bcode\b|claude code|codemender|t-sql|pl/pgsql|fable 5|should i even learn to code|run code on google cloud"),
        ("Migration / Modernisation", r"migrat|moderniz|refactor|transfer appliance"),
        ("Cloud Hub / Console", r"cloud hub|all products page|\bconsole\b"),
        ("Google Cloud Marketplace", r"marketplace|bitnami"),
        ("Coûts / Billing / FinOps", r"\bbilling\b|\bpricing\b|\bcosts?\b|finops|discounts?"),
    ]),
    ("Applications & Intégration", [
        ("Apigee / API Management", r"apigee|\bapis?\b"),
        ("Firebase", r"firebase"),
        ("AppSheet", r"appsheet"),
        ("Google Workspace", r"workspace|g suite"),
        ("Google Earth Engine", r"earth engine"),
        ("UI/UX Design", r"user interface|design tool"),
        ("SaaS", r"\bsaas\b"),
        ("IoT", r"\biot\b"),
        ("Blockchain", r"blockchain|band protocol"),
        ("Games / Divertissement", r"\bgames?\b|gaming|arcade|theme parks?|\bsports\b"),
        ("Manufacturing / Industrie", r"manufacturing|\bfactory\b|edge.{0,20}industr"),
    ]),
    ("Communauté & Événements", [
        ("Événements / Keynotes", r"\bnext\b\s*20\d\d|cloud onair|google cloud live|\bkeynote\b|\bsummit\b|googlecloudnext|next live|\bgdc\b|webinar|livestream|developer day|next '\d\d|rewind|innovators hive|fireside chat|agent clinic|hackathon|\bchallenge\b|\btrailer\b|i/o 20\d\d|\brsvp\b|in-person events"),
        ("Podcast / Interviews", r"podcast|\bepisode\s*\d|q&a\b|fireside chat|the agent factory"),
        ("Carrière / Culture", r"#shorts|cloud job|career|from .* to .*(google|tech|cloud)|pivoted|wrestling|beauty queen|day in the life|developer program|googlers|hidden gems|go-to learning|beginner.s tip|inclusive|women.? leaders|get a job|without a degree"),
        ("Documentation / Aide", r"where can i find|documentation|quickstart|learning path|skill badges?|fit assessment|get started docs|resources for|slow data|store data on google cloud|get started with cloud|three-step overview|cloud pso|experience management|data journeys"),
        ("Vie de la chaîne", r"subscribers|thank you for|welcome to google cloud tech|behind the scenes|new .* homepage|new cloud series|reached 1 million|fun cloud next|cloud innovators|light up the new year|watch the full video|thank you cloud community|takes over the google cloud tech channel"),
        ("Certifications Google Cloud", r"certif"),
        ("Certification Professional Data Engineer", r"professional data engineer|data engineer certif"),
        ("Témoignages clients / Études de cas", r"with google cloud\b|and google cloud\b|\bhow \w+ (scales?|manages?|built|uses?|transformed|analyzes?|scaled|reached|saved|serves?)\b|customer (experience|retention)|case stud|\bwp engine\b|\bukg\b|\bbroadcom\b|\bvirgin media\b|\bhcl software\b|\bitopia\b|\bcitrix\b|\beyecarelive\b|l.oreal|\buber\b|square enix|playstation|google photos"),
        ("Sciences & Biologie", r"alphafold|\bnasa\b|\bbiology\b|\bmedicine\b"),
        ("Programmes Startups", r"startup programs?|technical guides for startups|why startups choose|startups shipping|startup founder"),
        ("Présentation générale Google Cloud", r"^what is google cloud\??$|^introduction to google cloud$|the cloud built for developers|why (startups choose|do businesses go serverless)|google cloud tech$"),
        ("Nouveautés Google Cloud", r"what.s (new|next) (in|for) google cloud|course preview|google cloud data analytics"),
    ]),
]

# Titres isolés ne matchant aucune regex générique — tag(s) attribué(s) à la main.
MANUAL_OVERRIDES = {
    "How to enable app management for Google Cloud folder": ["IAM / Identity / Policy"],
    "How to delete a project": ["Documentation / Aide"],
    "Improving containerized development using Google Cloud": ["Kubernetes / GKE"],
    "How can organizations get started with cloud": ["Documentation / Aide"],
    "How to store data on Google Cloud": ["Documentation / Aide"],
    "Breaking records: 100 trillion digits of Pi": ["Compute Engine / VMs"],
    "How to run code on Google Cloud": ["Frameworks, langages & outils de code"],
    "How to get a job in cloud without a degree": ["Carrière / Culture"],
    "What's new in Go": ["Frameworks, langages & outils de code"],
    "Extract value with assisted analytics": ["Machine Learning (général)"],
    "He built a voice controlled drone to avoid using a remote! 🤯✈️": ["IA : applications & chatbots"],
    "Building apps on Google Cloud": ["Présentation générale Google Cloud"],
}

ALL_TAGS = [tag for _, tags in GROUPS for tag, _ in tags]
assert len(ALL_TAGS) == len(set(ALL_TAGS)), "tag en double dans GROUPS"
for _title, _tags in MANUAL_OVERRIDES.items():
    for _t in _tags:
        assert _t in ALL_TAGS, f"MANUAL_OVERRIDES : tag inconnu {_t!r}"
