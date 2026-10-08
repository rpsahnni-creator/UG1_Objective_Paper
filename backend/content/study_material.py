"""
Bilingual study material for the 3 chapters.
Readable, exam-oriented notes. English + Hindi (Devanagari).
"""

STUDY_MATERIAL = [
    {
        "chapter_id": "unit1",
        "title_en": "UNIT-I: Introduction to Computers",
        "title_hi": "इकाई-I: कंप्यूटर का परिचय",
        "sections": [
            {
                "heading_en": "1. Computer: Characteristics and Capabilities",
                "heading_hi": "1. कंप्यूटर: विशेषताएँ और क्षमताएँ",
                "body_en": (
                    "A computer is an electronic device that accepts data as input, processes "
                    "it according to a set of stored instructions (program), and produces useful "
                    "information as output. Key characteristics include: Speed (processes millions "
                    "of instructions per second), Accuracy (produces error-free output when inputs "
                    "and instructions are correct), Diligence (does not get tired or bored), "
                    "Versatility (performs many different tasks), Storage (holds large volumes of "
                    "data), and Automation (executes long tasks without human intervention)."
                ),
                "body_hi": (
                    "कंप्यूटर एक इलेक्ट्रॉनिक उपकरण है जो डेटा को इनपुट के रूप में लेता है, संग्रहित "
                    "निर्देशों (प्रोग्राम) के अनुसार उसे संसाधित करता है और उपयोगी सूचना आउटपुट के रूप में "
                    "देता है। मुख्य विशेषताएँ हैं: तेज़ी (लाखों निर्देश प्रति सेकंड), सटीकता (सही इनपुट पर "
                    "त्रुटिरहित परिणाम), कर्मठता (थकता नहीं), बहुमुखी प्रतिभा (अनेक कार्य कर सकता है), "
                    "भंडारण (बड़ी मात्रा में डेटा रखता है) और स्वचालन (मानव हस्तक्षेप के बिना लंबे कार्य)।"
                ),
            },
            {
                "heading_en": "2. Hardware and Software — Block Diagram",
                "heading_hi": "2. हार्डवेयर और सॉफ्टवेयर — ब्लॉक आरेख",
                "body_en": (
                    "Hardware refers to the physical parts you can touch — the CPU, memory, "
                    "monitor, keyboard, etc. Software is the set of instructions that tell the "
                    "hardware what to do. The classic block diagram of a computer has four "
                    "functional blocks:\n"
                    "• Input Unit — accepts data from the user (keyboard, mouse, scanner).\n"
                    "• Central Processing Unit (CPU) — the 'brain', containing the Control Unit "
                    "(CU) that directs operations, and the Arithmetic Logic Unit (ALU) that "
                    "performs calculations and comparisons.\n"
                    "• Memory Unit — stores data and instructions during processing (primary) "
                    "and for long-term use (secondary).\n"
                    "• Output Unit — presents the processed information (monitor, printer, "
                    "speaker)."
                ),
                "body_hi": (
                    "हार्डवेयर कंप्यूटर के भौतिक भाग हैं जिन्हें छुआ जा सकता है — CPU, मेमोरी, मॉनिटर, "
                    "कीबोर्ड आदि। सॉफ्टवेयर निर्देशों का समूह है जो हार्डवेयर को बताता है कि क्या करना है। "
                    "कंप्यूटर के ब्लॉक आरेख में चार मुख्य इकाइयाँ होती हैं:\n"
                    "• इनपुट इकाई — उपयोगकर्ता से डेटा लेती है (कीबोर्ड, माउस, स्कैनर)।\n"
                    "• केंद्रीय प्रसंस्करण इकाई (CPU) — 'मस्तिष्क'; इसमें नियंत्रण इकाई (CU) संचालन का "
                    "निर्देशन करती है और अंकगणितीय-तर्क इकाई (ALU) गणना व तुलना करती है।\n"
                    "• मेमोरी इकाई — प्रसंस्करण के समय (प्राथमिक) और दीर्घकालिक (द्वितीयक) डेटा रखती है।\n"
                    "• आउटपुट इकाई — प्रसंस्कृत सूचना दिखाती है (मॉनिटर, प्रिंटर, स्पीकर)।"
                ),
            },
            {
                "heading_en": "3. Types, Purpose and Components",
                "heading_hi": "3. कंप्यूटरों के प्रकार, उद्देश्य और घटक",
                "body_en": (
                    "By size and power: Microcomputer (PC, laptop), Minicomputer (small business "
                    "servers), Mainframe (large enterprise systems), Supercomputer (scientific "
                    "simulations like PARAM). By purpose: General-purpose (daily tasks) and "
                    "Special-purpose (e.g., ATM, traffic signal). Core components inside the "
                    "cabinet are the Motherboard, CPU, RAM, Hard disk / SSD, Power supply (SMPS) "
                    "and expansion cards."
                ),
                "body_hi": (
                    "आकार और शक्ति के अनुसार: माइक्रो कंप्यूटर (PC, लैपटॉप), मिनी कंप्यूटर (छोटे व्यावसायिक "
                    "सर्वर), मेनफ्रेम (बड़े संगठन), सुपर कंप्यूटर (वैज्ञानिक गणनाएँ, जैसे PARAM)। उद्देश्य के "
                    "अनुसार: सामान्य उद्देश्य और विशिष्ट उद्देश्य (जैसे ATM, ट्रैफ़िक सिग्नल)। कैबिनेट के "
                    "अंदर मुख्य घटक: मदरबोर्ड, CPU, RAM, हार्ड डिस्क/SSD, पावर सप्लाई (SMPS) और "
                    "विस्तार कार्ड होते हैं।"
                ),
            },
            {
                "heading_en": "4. Generations of Computers",
                "heading_hi": "4. कंप्यूटरों की पीढ़ियाँ",
                "body_en": (
                    "• 1st Gen (1946-59): Vacuum tubes — ENIAC, UNIVAC. Huge, slow, hot.\n"
                    "• 2nd Gen (1959-65): Transistors — smaller, faster, more reliable.\n"
                    "• 3rd Gen (1965-71): Integrated Circuits (ICs) — IBM 360 series.\n"
                    "• 4th Gen (1971-80): Microprocessors (VLSI) — Intel 8080, personal "
                    "computers born.\n"
                    "• 5th Gen (1980-present): ULSI, parallel processing, AI focus."
                ),
                "body_hi": (
                    "• पहली पीढ़ी (1946-59): वैक्यूम ट्यूब — ENIAC, UNIVAC। बड़े, धीमे, गर्म।\n"
                    "• दूसरी पीढ़ी (1959-65): ट्रांज़िस्टर — छोटे, तेज़, विश्वसनीय।\n"
                    "• तीसरी पीढ़ी (1965-71): इंटीग्रेटेड सर्किट (IC) — IBM 360।\n"
                    "• चौथी पीढ़ी (1971-80): माइक्रोप्रोसेसर (VLSI) — Intel 8080, PC का जन्म।\n"
                    "• पाँचवीं पीढ़ी (1980-अब): ULSI, समानांतर प्रसंस्करण, AI पर ध्यान।"
                ),
            },
            {
                "heading_en": "5. Functional Units — CPU in Detail",
                "heading_hi": "5. कार्यात्मक इकाइयाँ — CPU विस्तार से",
                "body_en": (
                    "The CPU has three parts: the Control Unit (CU) which fetches instructions "
                    "and controls the flow; the Arithmetic Logic Unit (ALU) which performs "
                    "arithmetic (+, -, *, /) and logical (AND, OR, NOT, comparisons) operations; "
                    "and Registers which are tiny, very fast storage used during execution "
                    "(accumulator, program counter, instruction register)."
                ),
                "body_hi": (
                    "CPU के तीन भाग हैं: नियंत्रण इकाई (CU) जो निर्देश लाती है और प्रवाह नियंत्रित करती "
                    "है; अंकगणितीय-तर्क इकाई (ALU) जो अंकगणितीय (+,-,*,/) और तार्किक (AND, OR, NOT, "
                    "तुलना) कार्य करती है; और रजिस्टर जो निष्पादन के समय बहुत तेज़, छोटे संग्रहक होते हैं "
                    "(एक्यूम्यूलेटर, प्रोग्राम काउंटर, इंस्ट्रक्शन रजिस्टर)।"
                ),
            },
            {
                "heading_en": "6. Number Systems and Conversions",
                "heading_hi": "6. संख्या पद्धतियाँ और रूपांतरण",
                "body_en": (
                    "Computers internally use binary (base-2, digits 0 and 1). Humans commonly "
                    "use decimal (base-10). For compactness, programmers also use octal (base-8) "
                    "and hexadecimal (base-16, digits 0-9 and A-F).\n\n"
                    "Example: Decimal 25 → Binary 11001 (because 16+8+1=25) → Octal 31 → Hex 19.\n"
                    "To convert decimal to any base, divide repeatedly by the base and read the "
                    "remainders in reverse. To convert back, multiply each digit by the base "
                    "raised to its position."
                ),
                "body_hi": (
                    "कंप्यूटर आंतरिक रूप से बाइनरी (आधार-2, अंक 0 और 1) का उपयोग करता है। मनुष्य आमतौर "
                    "पर दशमलव (आधार-10) उपयोग करते हैं। संक्षिप्तता के लिए प्रोग्रामर ऑक्टल (आधार-8) और "
                    "हेक्साडेसिमल (आधार-16, अंक 0-9 और A-F) भी उपयोग करते हैं।\n\n"
                    "उदाहरण: दशमलव 25 → बाइनरी 11001 (क्योंकि 16+8+1=25) → ऑक्टल 31 → हेक्स 19।\n"
                    "दशमलव से किसी आधार में बदलने के लिए बार-बार उस आधार से भाग दें और शेषफल को "
                    "उल्टे क्रम में पढ़ें। वापस बदलने के लिए प्रत्येक अंक को उसके स्थान पर आधार की घात से "
                    "गुणा करें।"
                ),
            },
        ],
    },
    {
        "chapter_id": "unit2",
        "title_en": "UNIT-II: Hardware, Software & Office Applications",
        "title_hi": "इकाई-II: हार्डवेयर, सॉफ्टवेयर व ऑफ़िस अनुप्रयोग",
        "sections": [
            {
                "heading_en": "1. Input and Output Devices",
                "heading_hi": "1. इनपुट और आउटपुट उपकरण",
                "body_en": (
                    "Input devices feed data into the computer: keyboard (text), mouse / "
                    "touchpad (pointing), scanner (digitizing documents), microphone (audio), "
                    "webcam (video), barcode / QR reader, joystick, light pen, biometric "
                    "sensors. Output devices present results: monitor / LCD / LED (visual), "
                    "printer (hard copy — dot-matrix, inkjet, laser), plotter (large drawings), "
                    "speakers / headphones (audio), projector."
                ),
                "body_hi": (
                    "इनपुट उपकरण कंप्यूटर में डेटा डालते हैं: कीबोर्ड (पाठ), माउस/टचपैड (संकेत), स्कैनर "
                    "(डिजिटलीकरण), माइक्रोफ़ोन (ध्वनि), वेबकैम (वीडियो), बारकोड/QR रीडर, जॉयस्टिक, "
                    "लाइट पेन, बायोमेट्रिक सेंसर। आउटपुट उपकरण परिणाम दिखाते हैं: मॉनिटर/LCD/LED "
                    "(दृश्य), प्रिंटर (हार्ड कॉपी — डॉट-मैट्रिक्स, इंकजेट, लेज़र), प्लॉटर (बड़े चित्र), "
                    "स्पीकर/हेडफ़ोन (ध्वनि), प्रोजेक्टर।"
                ),
            },
            {
                "heading_en": "2. Storage and Memory Hierarchy",
                "heading_hi": "2. संग्रहण और मेमोरी पदानुक्रम",
                "body_en": (
                    "Memory is organised in a hierarchy from fastest and smallest to slowest "
                    "and largest:\n"
                    "• Registers (inside CPU, bytes, nanoseconds)\n"
                    "• Cache (L1/L2/L3, KB-MB)\n"
                    "• Primary / Main memory — RAM (volatile, GB) and ROM (non-volatile, "
                    "firmware)\n"
                    "• Secondary storage — Hard Disk (HDD), Solid State Drive (SSD), Optical "
                    "disks (CD/DVD/Blu-ray), USB flash drives, Magnetic tape (archival)\n"
                    "RAM types: SRAM (fast, costly, cache) and DRAM (slower, cheaper, main "
                    "memory). ROM types: PROM, EPROM, EEPROM."
                ),
                "body_hi": (
                    "मेमोरी एक पदानुक्रम में व्यवस्थित है, सबसे तेज़/छोटे से सबसे धीमे/बड़े तक:\n"
                    "• रजिस्टर (CPU के अंदर, बाइट, नैनोसेकंड)\n"
                    "• कैश (L1/L2/L3, KB-MB)\n"
                    "• प्राथमिक/मुख्य मेमोरी — RAM (वोलेटाइल, GB) और ROM (नॉन-वोलेटाइल, फ़र्मवेयर)\n"
                    "• द्वितीयक संग्रहण — हार्ड डिस्क (HDD), SSD, ऑप्टिकल डिस्क (CD/DVD/Blu-ray), "
                    "USB फ़्लैश ड्राइव, मैग्नेटिक टेप (संग्रहण)\n"
                    "RAM के प्रकार: SRAM (तेज़, महँगा, कैश) और DRAM (धीमा, सस्ता, मुख्य)। ROM के "
                    "प्रकार: PROM, EPROM, EEPROM।"
                ),
            },
            {
                "heading_en": "3. System vs Application Software",
                "heading_hi": "3. सिस्टम बनाम एप्लिकेशन सॉफ़्टवेयर",
                "body_en": (
                    "System software manages the hardware and provides a platform for other "
                    "programs — Operating Systems (Windows, Linux, macOS, Android), device "
                    "drivers, utilities, compilers and assemblers. Application software is built "
                    "for end-user tasks — MS Word, Excel, PowerPoint, browsers, media players, "
                    "games. The OS core jobs are: process management, memory management, file "
                    "management, device management, and user interface."
                ),
                "body_hi": (
                    "सिस्टम सॉफ़्टवेयर हार्डवेयर को प्रबंधित करता है और अन्य प्रोग्रामों के लिए मंच देता है — "
                    "ऑपरेटिंग सिस्टम (Windows, Linux, macOS, Android), डिवाइस ड्राइवर, यूटिलिटीज़, "
                    "कंपाइलर और असेंबलर। एप्लिकेशन सॉफ़्टवेयर अंतिम-उपयोगकर्ता के कार्यों के लिए होता है — "
                    "MS Word, Excel, PowerPoint, ब्राउज़र, मीडिया प्लेयर, गेम। OS के मुख्य कार्य: "
                    "प्रोसेस प्रबंधन, मेमोरी प्रबंधन, फ़ाइल प्रबंधन, उपकरण प्रबंधन और यूज़र इंटरफ़ेस।"
                ),
            },
            {
                "heading_en": "4. MS Word — Document Editing",
                "heading_hi": "4. MS Word — दस्तावेज़ संपादन",
                "body_en": (
                    "MS Word is a word processor used to create, edit, format and print "
                    "documents. Key features: Ribbon with Home/Insert/Layout/Review tabs, "
                    "formatting (font, size, bold, italic, alignment), paragraph styles, "
                    "bullets and numbering, tables, headers / footers, page numbers, mail "
                    "merge, spell-check, Find & Replace, track changes, and saving in .docx / "
                    ".pdf formats."
                ),
                "body_hi": (
                    "MS Word एक वर्ड प्रोसेसर है जिसका उपयोग दस्तावेज़ बनाने, संपादित करने, प्रारूपित "
                    "करने और छापने के लिए होता है। मुख्य सुविधाएँ: Home/Insert/Layout/Review टैब "
                    "वाला रिबन, स्वरूपण (फ़ॉन्ट, आकार, बोल्ड, इटैलिक, संरेखण), अनुच्छेद शैलियाँ, बुलेट/"
                    "संख्या, तालिकाएँ, हेडर/फ़ुटर, पेज नंबर, मेल मर्ज, स्पेल-चेक, Find & Replace, "
                    "ट्रैक चेंज, तथा .docx/.pdf में सहेजना।"
                ),
            },
            {
                "heading_en": "5. MS Excel — Data Handling",
                "heading_hi": "5. MS Excel — डेटा प्रबंधन",
                "body_en": (
                    "Excel is a spreadsheet program organised into Workbooks → Sheets → Cells. "
                    "Each cell has a reference (A1). Core formulas: =SUM(A1:A10), =AVERAGE, "
                    "=MIN, =MAX, =COUNT, =IF(logical, true, false), =VLOOKUP. Features: cell "
                    "formatting, sorting, filtering, pivot tables, charts (bar, line, pie), "
                    "conditional formatting and data validation."
                ),
                "body_hi": (
                    "Excel एक स्प्रेडशीट प्रोग्राम है जो वर्कबुक → शीट → सेल में संगठित होता है। हर सेल का "
                    "संदर्भ होता है (A1)। मुख्य सूत्र: =SUM(A1:A10), =AVERAGE, =MIN, =MAX, =COUNT, "
                    "=IF(शर्त, सही, गलत), =VLOOKUP। सुविधाएँ: सेल स्वरूपण, क्रमबद्धता, छानबीन, "
                    "पिवट टेबल, चार्ट (बार, लाइन, पाई), सशर्त स्वरूपण और डेटा सत्यापन।"
                ),
            },
            {
                "heading_en": "6. MS PowerPoint — Presentations",
                "heading_hi": "6. MS PowerPoint — प्रस्तुतियाँ",
                "body_en": (
                    "PowerPoint creates slide shows for teaching, meetings and conferences. A "
                    "presentation is a sequence of Slides. Features: slide layouts and themes, "
                    "inserting text / images / shapes / charts / videos, slide master, "
                    "transitions between slides, animations on objects, speaker notes and "
                    "running the show (F5)."
                ),
                "body_hi": (
                    "PowerPoint शिक्षण, बैठकों और सम्मेलनों के लिए स्लाइड शो बनाता है। एक प्रस्तुति "
                    "स्लाइडों का क्रम होती है। सुविधाएँ: स्लाइड लेआउट व थीम, टेक्स्ट/चित्र/आकृति/चार्ट/"
                    "वीडियो डालना, स्लाइड मास्टर, स्लाइडों के बीच ट्रांज़िशन, वस्तुओं पर एनिमेशन, "
                    "वक्ता-नोट्स तथा प्रस्तुति चलाना (F5)।"
                ),
            },
        ],
    },
    {
        "chapter_id": "unit3",
        "title_en": "UNIT-III: Networking and Internet",
        "title_hi": "इकाई-III: नेटवर्किंग और इंटरनेट",
        "sections": [
            {
                "heading_en": "1. Computer Network — Definition and Need",
                "heading_hi": "1. कंप्यूटर नेटवर्क — परिभाषा और आवश्यकता",
                "body_en": (
                    "A computer network is a group of two or more computers connected together "
                    "to share resources (files, printers, internet) and exchange data. Need: "
                    "resource sharing, communication (email, chat, video calls), centralised "
                    "data management, cost reduction, reliability through redundancy, and "
                    "remote access."
                ),
                "body_hi": (
                    "कंप्यूटर नेटवर्क दो या अधिक कंप्यूटरों का समूह है जो संसाधनों (फ़ाइल, प्रिंटर, इंटरनेट) "
                    "को साझा करने और डेटा का आदान-प्रदान करने के लिए जुड़े रहते हैं। आवश्यकता: संसाधन "
                    "साझा करना, संचार (ईमेल, चैट, वीडियो कॉल), केंद्रीकृत डेटा प्रबंधन, लागत में कमी, "
                    "विश्वसनीयता और दूरस्थ पहुँच।"
                ),
            },
            {
                "heading_en": "2. Types of Networks — LAN, MAN, WAN",
                "heading_hi": "2. नेटवर्क के प्रकार — LAN, MAN, WAN",
                "body_en": (
                    "• LAN (Local Area Network) — within a building or campus, very fast "
                    "(100 Mbps–10 Gbps), e.g., office or lab network.\n"
                    "• MAN (Metropolitan Area Network) — spans a city, e.g., cable TV or city-"
                    "wide Wi-Fi.\n"
                    "• WAN (Wide Area Network) — spans countries or the world, the Internet is "
                    "the largest WAN. Also: PAN (personal, Bluetooth) and CAN (campus)."
                ),
                "body_hi": (
                    "• LAN (स्थानीय क्षेत्र नेटवर्क) — भवन/परिसर के अंदर, बहुत तेज़ (100 Mbps–10 Gbps), "
                    "जैसे ऑफ़िस या प्रयोगशाला।\n"
                    "• MAN (महानगरीय क्षेत्र नेटवर्क) — शहर भर में, जैसे केबल TV या सिटी Wi-Fi।\n"
                    "• WAN (विस्तृत क्षेत्र नेटवर्क) — देशों/विश्व भर में, इंटरनेट सबसे बड़ा WAN है। साथ ही: "
                    "PAN (व्यक्तिगत, ब्लूटूथ) और CAN (परिसर)।"
                ),
            },
            {
                "heading_en": "3. Network Devices",
                "heading_hi": "3. नेटवर्क उपकरण",
                "body_en": (
                    "• Modem — modulates/demodulates signals between digital computer and "
                    "analog phone / cable line (gives Internet access).\n"
                    "• Hub — a dumb multi-port repeater; broadcasts to all ports (obsolete).\n"
                    "• Switch — intelligently forwards data only to the destination port using "
                    "MAC addresses (Layer-2).\n"
                    "• Router — connects different networks and forwards packets using IP "
                    "addresses (Layer-3); your home Wi-Fi box is a router + switch + modem."
                ),
                "body_hi": (
                    "• मॉडम — डिजिटल कंप्यूटर और एनालॉग फ़ोन/केबल लाइन के बीच सिग्नल मॉडुलेट/डिमॉडुलेट "
                    "करता है (इंटरनेट पहुँच देता है)।\n"
                    "• हब — साधारण मल्टी-पोर्ट रिपीटर; सभी पोर्ट पर प्रसारण (अब पुराना)।\n"
                    "• स्विच — MAC पते का उपयोग करके डेटा केवल सही पोर्ट पर भेजता है (परत-2)।\n"
                    "• राउटर — भिन्न नेटवर्कों को जोड़ता है और IP पते का उपयोग करके पैकेट अग्रेषित करता "
                    "है (परत-3); आपका घरेलू Wi-Fi बॉक्स राउटर + स्विच + मॉडम का संयोजन है।"
                ),
            },
            {
                "heading_en": "4. IP Addressing and DNS",
                "heading_hi": "4. IP पता और DNS",
                "body_en": (
                    "An IP address is a unique numeric identifier for a device on a network. "
                    "IPv4 uses 32 bits (e.g., 192.168.1.1); IPv6 uses 128 bits. Private ranges "
                    "(10.x, 172.16-31.x, 192.168.x) are used inside LANs. DNS (Domain Name "
                    "System) translates human-friendly names like www.google.com into IP "
                    "addresses — it is the 'phone book' of the Internet."
                ),
                "body_hi": (
                    "IP पता नेटवर्क पर किसी उपकरण का विशिष्ट संख्यात्मक पहचानकर्ता है। IPv4 32-बिट का "
                    "होता है (जैसे 192.168.1.1); IPv6 128-बिट। निजी श्रेणियाँ (10.x, 172.16-31.x, "
                    "192.168.x) LAN के अंदर उपयोग होती हैं। DNS (डोमेन नेम सिस्टम) "
                    "www.google.com जैसे नामों को IP पते में बदलता है — यह इंटरनेट की 'टेलीफ़ोन "
                    "डायरेक्टरी' है।"
                ),
            },
            {
                "heading_en": "5. HTTP, Email and Web Browsing",
                "heading_hi": "5. HTTP, ईमेल और वेब ब्राउज़िंग",
                "body_en": (
                    "HTTP (HyperText Transfer Protocol) is the protocol browsers use to request "
                    "web pages from servers; HTTPS adds TLS encryption for security. Email uses "
                    "SMTP to send and POP3 / IMAP to receive. A web browser (Chrome, Firefox, "
                    "Edge) renders HTML/CSS/JS. Search engines (Google, Bing, DuckDuckGo) crawl "
                    "and index the web and let users find pages by keywords."
                ),
                "body_hi": (
                    "HTTP (HyperText Transfer Protocol) वह प्रोटोकॉल है जिसका उपयोग ब्राउज़र सर्वर से "
                    "वेब पेज माँगने के लिए करते हैं; HTTPS इसमें TLS एन्क्रिप्शन जोड़कर सुरक्षा देता है। "
                    "ईमेल भेजने के लिए SMTP और प्राप्त करने के लिए POP3/IMAP का उपयोग होता है। "
                    "वेब ब्राउज़र (Chrome, Firefox, Edge) HTML/CSS/JS प्रस्तुत करता है। खोज इंजन "
                    "(Google, Bing, DuckDuckGo) वेब को क्रॉल करके अनुक्रमित करते हैं और उपयोगकर्ताओं "
                    "को कीवर्ड से पेज ढूँढने देते हैं।"
                ),
            },
            {
                "heading_en": "6. Emerging Technologies — AI, Big Data, Blockchain",
                "heading_hi": "6. उभरती प्रौद्योगिकियाँ — AI, बिग डेटा, ब्लॉकचेन",
                "body_en": (
                    "• Artificial Intelligence (AI) — machines performing tasks that normally "
                    "need human intelligence (vision, speech, decisions). Sub-fields: Machine "
                    "Learning, Deep Learning, NLP.\n"
                    "• Big Data — datasets so large and fast that traditional tools fail; the "
                    "'5 Vs': Volume, Velocity, Variety, Veracity, Value. Tools: Hadoop, Spark.\n"
                    "• Blockchain — a distributed, tamper-resistant digital ledger of linked "
                    "blocks secured by cryptographic hashes; the technology behind cryptocurrencies "
                    "like Bitcoin, and also used for supply-chain and healthcare records."
                ),
                "body_hi": (
                    "• कृत्रिम बुद्धिमत्ता (AI) — मशीनें वे कार्य करती हैं जिनके लिए सामान्यतः मानव-बुद्धि "
                    "चाहिए (दृष्टि, वाणी, निर्णय)। उप-क्षेत्र: मशीन लर्निंग, डीप लर्निंग, NLP।\n"
                    "• बिग डेटा — इतने बड़े व तेज़ डेटासेट कि पारंपरिक उपकरण नाकाम हों; '5 V': Volume, "
                    "Velocity, Variety, Veracity, Value। उपकरण: Hadoop, Spark।\n"
                    "• ब्लॉकचेन — एक वितरित, छेड़छाड़-रोधी डिजिटल बहीखाता, जो क्रिप्टोग्राफ़िक हैश से "
                    "जुड़े ब्लॉकों का क्रम है; बिटकॉइन जैसी क्रिप्टो-मुद्राओं की तकनीक, आपूर्ति-श्रृंखला व "
                    "स्वास्थ्य रिकॉर्ड में भी उपयोगी।"
                ),
            },
        ],
    },
]
