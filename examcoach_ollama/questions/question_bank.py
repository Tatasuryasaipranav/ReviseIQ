"""
question_bank.py — Curated quiz questions for JEE, EAPCET, NEET, GATE, UPSC, CAT
Each question has: id, exam, subject, topic, difficulty, question, options (A-D), answer, explanation
"""

QUESTIONS = [

  # ─── JEE PHYSICS ───────────────────────────────────────────────────────────
  {"id":"JEE_PHY_001","exam":"JEE","subject":"Physics","topic":"Kinematics","difficulty":"medium",
   "question":"A ball is thrown vertically upward with velocity 20 m/s. The maximum height reached is (g = 10 m/s²):",
   "options":{"A":"10 m","B":"20 m","C":"30 m","D":"40 m"},"answer":"B",
   "explanation":"Using v² = u² − 2gh → 0 = 400 − 20h → h = 20 m"},

  {"id":"JEE_PHY_002","exam":"JEE","subject":"Physics","topic":"Newton's Laws","difficulty":"medium",
   "question":"A block of mass 5 kg is placed on a frictionless surface. A force of 20 N is applied. The acceleration is:",
   "options":{"A":"2 m/s²","B":"4 m/s²","C":"5 m/s²","D":"10 m/s²"},"answer":"B",
   "explanation":"F = ma → a = F/m = 20/5 = 4 m/s²"},

  {"id":"JEE_PHY_003","exam":"JEE","subject":"Physics","topic":"Work & Energy","difficulty":"easy",
   "question":"The work done by a force of 10 N displacing an object by 5 m at 60° to the force direction is:",
   "options":{"A":"25 J","B":"50 J","C":"43.3 J","D":"86.6 J"},"answer":"A",
   "explanation":"W = Fd·cosθ = 10 × 5 × cos60° = 50 × 0.5 = 25 J"},

  {"id":"JEE_PHY_004","exam":"JEE","subject":"Physics","topic":"Thermodynamics","difficulty":"hard",
   "question":"In an adiabatic process for an ideal gas, which relation holds? (γ = Cp/Cv):",
   "options":{"A":"TV^γ = constant","B":"TV^(γ-1) = constant","C":"T^γ V = constant","D":"PV = constant"},
   "answer":"B","explanation":"For adiabatic: PV^γ = const. Using ideal gas law, TV^(γ-1) = constant"},

  {"id":"JEE_PHY_005","exam":"JEE","subject":"Physics","topic":"Electrostatics","difficulty":"medium",
   "question":"The electric field inside a uniformly charged hollow spherical shell is:",
   "options":{"A":"Maximum at centre","B":"Zero everywhere","C":"Same as outside","D":"Inversely proportional to r²"},
   "answer":"B","explanation":"By Gauss's law, no enclosed charge inside → E = 0 everywhere inside"},

  {"id":"JEE_PHY_006","exam":"JEE","subject":"Physics","topic":"Optics","difficulty":"medium",
   "question":"A convex lens of focal length 20 cm forms image of object at 30 cm from lens. Image distance is:",
   "options":{"A":"30 cm","B":"60 cm","C":"120 cm","D":"−60 cm"},"answer":"B",
   "explanation":"1/v − 1/u = 1/f → 1/v − 1/(−30) = 1/20 → 1/v = 1/20 − 1/30 = 1/60 → v = 60 cm"},

  {"id":"JEE_PHY_007","exam":"JEE","subject":"Physics","topic":"Waves","difficulty":"easy",
   "question":"The frequency of a wave is 500 Hz and its wavelength is 0.4 m. The speed of wave is:",
   "options":{"A":"100 m/s","B":"125 m/s","C":"200 m/s","D":"250 m/s"},"answer":"C",
   "explanation":"v = fλ = 500 × 0.4 = 200 m/s"},

  {"id":"JEE_PHY_008","exam":"JEE","subject":"Physics","topic":"Modern Physics","difficulty":"hard",
   "question":"The de Broglie wavelength of an electron accelerated through 100 V is approximately:",
   "options":{"A":"0.123 nm","B":"1.23 nm","C":"12.3 nm","D":"0.0123 nm"},"answer":"A",
   "explanation":"λ = h/√(2meV) = 12.27/√100 Å = 1.227 Å ≈ 0.123 nm"},

  # ─── JEE CHEMISTRY ─────────────────────────────────────────────────────────
  {"id":"JEE_CHE_001","exam":"JEE","subject":"Chemistry","topic":"Chemical Bonding","difficulty":"easy",
   "question":"The hybridisation of carbon in CH₄ is:",
   "options":{"A":"sp","B":"sp²","C":"sp³","D":"sp³d"},"answer":"C",
   "explanation":"Carbon in methane has 4 sigma bonds, all single bonds → sp³ hybridisation"},

  {"id":"JEE_CHE_002","exam":"JEE","subject":"Chemistry","topic":"Thermodynamics","difficulty":"medium",
   "question":"For a spontaneous process at constant T and P, which condition must hold?",
   "options":{"A":"ΔG > 0","B":"ΔG < 0","C":"ΔG = 0","D":"ΔH < 0 always"},"answer":"B",
   "explanation":"Gibbs free energy criterion: ΔG < 0 for spontaneous processes at constant T and P"},

  {"id":"JEE_CHE_003","exam":"JEE","subject":"Chemistry","topic":"Electrochemistry","difficulty":"medium",
   "question":"Standard EMF of a cell is related to ΔG° by:",
   "options":{"A":"ΔG° = nFE°","B":"ΔG° = −nFE°","C":"ΔG° = nRTE°","D":"ΔG° = −RT ln E°"},
   "answer":"B","explanation":"ΔG° = −nFE° where n = electrons transferred, F = Faraday constant"},

  {"id":"JEE_CHE_004","exam":"JEE","subject":"Chemistry","topic":"Organic Chemistry","difficulty":"hard",
   "question":"The product of reaction of benzene with CH₃Cl in presence of AlCl₃ is:",
   "options":{"A":"Chlorobenzene","B":"Toluene","C":"Benzaldehyde","D":"Benzyl chloride"},"answer":"B",
   "explanation":"Friedel-Crafts alkylation: Benzene + CH₃Cl/AlCl₃ → Toluene (methylbenzene)"},

  {"id":"JEE_CHE_005","exam":"JEE","subject":"Chemistry","topic":"Equilibrium","difficulty":"medium",
   "question":"For the reaction N₂ + 3H₂ ⇌ 2NH₃, increasing pressure will:",
   "options":{"A":"Shift equilibrium left","B":"Shift equilibrium right","C":"No effect","D":"Increase temperature"},
   "answer":"B","explanation":"4 moles gas → 2 moles. By Le Chatelier, increasing pressure favors fewer moles → shifts right"},

  # ─── JEE MATHEMATICS ───────────────────────────────────────────────────────
  {"id":"JEE_MAT_001","exam":"JEE","subject":"Mathematics","topic":"Calculus","difficulty":"medium",
   "question":"The derivative of sin(x²) with respect to x is:",
   "options":{"A":"cos(x²)","B":"2x·cos(x²)","C":"2x·sin(x²)","D":"cos(2x)"},"answer":"B",
   "explanation":"d/dx[sin(x²)] = cos(x²) · 2x by chain rule"},

  {"id":"JEE_MAT_002","exam":"JEE","subject":"Mathematics","topic":"Algebra","difficulty":"easy",
   "question":"The roots of x² − 5x + 6 = 0 are:",
   "options":{"A":"2, 3","B":"1, 6","C":"−2, −3","D":"2, −3"},"answer":"A",
   "explanation":"x² − 5x + 6 = (x−2)(x−3) = 0 → x = 2 or x = 3"},

  {"id":"JEE_MAT_003","exam":"JEE","subject":"Mathematics","topic":"Coordinate Geometry","difficulty":"medium",
   "question":"The distance between points (3, 4) and (0, 0) is:",
   "options":{"A":"3","B":"4","C":"5","D":"7"},"answer":"C",
   "explanation":"d = √(3² + 4²) = √(9+16) = √25 = 5"},

  {"id":"JEE_MAT_004","exam":"JEE","subject":"Mathematics","topic":"Probability","difficulty":"hard",
   "question":"Two dice are thrown. The probability that the sum is 7 is:",
   "options":{"A":"1/6","B":"1/12","C":"7/36","D":"5/36"},"answer":"A",
   "explanation":"Favourable outcomes: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6. Total = 36. P = 6/36 = 1/6"},

  {"id":"JEE_MAT_005","exam":"JEE","subject":"Mathematics","topic":"Trigonometry","difficulty":"easy",
   "question":"The value of sin(30°) + cos(60°) is:",
   "options":{"A":"0","B":"1","C":"√3/2","D":"√3"},"answer":"B",
   "explanation":"sin(30°) = 1/2, cos(60°) = 1/2 → sum = 1"},

  # ─── EAPCET PHYSICS ────────────────────────────────────────────────────────
  {"id":"EAP_PHY_001","exam":"EAPCET","subject":"Physics","topic":"Mechanics","difficulty":"medium",
   "question":"A stone is dropped from a height of 80 m. Time taken to reach ground is (g = 10 m/s²):",
   "options":{"A":"2 s","B":"4 s","C":"6 s","D":"8 s"},"answer":"B",
   "explanation":"h = ½gt² → 80 = ½×10×t² → t² = 16 → t = 4 s"},

  {"id":"EAP_PHY_002","exam":"EAPCET","subject":"Physics","topic":"Current Electricity","difficulty":"medium",
   "question":"Three resistors of 2Ω, 3Ω and 6Ω are connected in parallel. Effective resistance is:",
   "options":{"A":"1 Ω","B":"2 Ω","C":"3 Ω","D":"11 Ω"},"answer":"A",
   "explanation":"1/R = 1/2 + 1/3 + 1/6 = 3/6 + 2/6 + 1/6 = 6/6 = 1 → R = 1 Ω"},

  {"id":"EAP_PHY_003","exam":"EAPCET","subject":"Physics","topic":"Magnetism","difficulty":"hard",
   "question":"The SI unit of magnetic flux is:",
   "options":{"A":"Tesla","B":"Weber","C":"Gauss","D":"Henry"},"answer":"B",
   "explanation":"Magnetic flux Φ = B·A. Its SI unit is Weber (Wb) = V·s = kg·m²·A⁻¹·s⁻²"},

  # ─── EAPCET CHEMISTRY ──────────────────────────────────────────────────────
  {"id":"EAP_CHE_001","exam":"EAPCET","subject":"Chemistry","topic":"Atomic Structure","difficulty":"easy",
   "question":"The number of orbitals in the fourth shell (n=4) is:",
   "options":{"A":"4","B":"8","C":"16","D":"32"},"answer":"C",
   "explanation":"Number of orbitals = n² = 4² = 16"},

  {"id":"EAP_CHE_002","exam":"EAPCET","subject":"Chemistry","topic":"Periodic Table","difficulty":"easy",
   "question":"The element with highest electronegativity in periodic table is:",
   "options":{"A":"Oxygen","B":"Chlorine","C":"Nitrogen","D":"Fluorine"},"answer":"D",
   "explanation":"Fluorine (F) has the highest electronegativity (3.98 on Pauling scale)"},

  {"id":"EAP_CHE_003","exam":"EAPCET","subject":"Chemistry","topic":"Polymers","difficulty":"medium",
   "question":"Nylon-6,6 is formed by condensation of:",
   "options":{"A":"Hexamethylene diamine + Adipic acid","B":"Caprolactam","C":"Glycine + Alanine","D":"Ethylene glycol + Terephthalic acid"},
   "answer":"A","explanation":"Nylon-6,6 is formed by condensation polymerisation of hexamethylene diamine and adipic acid"},

  # ─── EAPCET MATHEMATICS ────────────────────────────────────────────────────
  {"id":"EAP_MAT_001","exam":"EAPCET","subject":"Mathematics","topic":"Matrices","difficulty":"medium",
   "question":"If A is a 3×3 matrix and |A| = 5, then |2A| is:",
   "options":{"A":"10","B":"20","C":"40","D":"160"},"answer":"C",
   "explanation":"|kA| = k^n · |A| for n×n matrix. |2A| = 2³ × 5 = 8 × 5 = 40"},

  {"id":"EAP_MAT_002","exam":"EAPCET","subject":"Mathematics","topic":"Complex Numbers","difficulty":"hard",
   "question":"The modulus of (3 + 4i) is:",
   "options":{"A":"3","B":"4","C":"5","D":"7"},"answer":"C",
   "explanation":"|3+4i| = √(3²+4²) = √(9+16) = √25 = 5"},

  # ─── NEET PHYSICS ──────────────────────────────────────────────────────────
  {"id":"NEET_PHY_001","exam":"NEET","subject":"Physics","topic":"Laws of Motion","difficulty":"easy",
   "question":"Newton's third law of motion states:",
   "options":{"A":"F = ma","B":"Every action has equal and opposite reaction",
               "C":"Body remains at rest unless acted upon","D":"Rate of change of momentum = Force"},"answer":"B",
   "explanation":"Newton's 3rd Law: For every action, there is an equal and opposite reaction"},

  {"id":"NEET_PHY_002","exam":"NEET","subject":"Physics","topic":"Fluid Mechanics","difficulty":"medium",
   "question":"Bernoulli's principle is based on conservation of:",
   "options":{"A":"Mass","B":"Momentum","C":"Energy","D":"Angular momentum"},"answer":"C",
   "explanation":"Bernoulli's equation is derived from conservation of energy in fluid flow"},

  {"id":"NEET_PHY_003","exam":"NEET","subject":"Physics","topic":"Thermodynamics","difficulty":"medium",
   "question":"In isothermal process, temperature remains constant. The internal energy of an ideal gas:",
   "options":{"A":"Increases","B":"Decreases","C":"Remains constant","D":"Becomes zero"},"answer":"C",
   "explanation":"For ideal gas, internal energy depends only on temperature. Isothermal → T constant → ΔU = 0"},

  # ─── NEET CHEMISTRY ────────────────────────────────────────────────────────
  {"id":"NEET_CHE_001","exam":"NEET","subject":"Chemistry","topic":"Biomolecules","difficulty":"medium",
   "question":"The monomer unit of DNA is:",
   "options":{"A":"Amino acid","B":"Nucleotide","C":"Glucose","D":"Fatty acid"},"answer":"B",
   "explanation":"DNA is a polymer of nucleotides. Each nucleotide = phosphate + sugar (deoxyribose) + nitrogenous base"},

  {"id":"NEET_CHE_002","exam":"NEET","subject":"Chemistry","topic":"Coordination Compounds","difficulty":"hard",
   "question":"The IUPAC name of [Cu(NH₃)₄]²⁺ is:",
   "options":{"A":"Copper tetraamine","B":"Tetraamminecopper(II)","C":"Tetrammine cupric","D":"Copper(II) tetramine"},
   "answer":"B","explanation":"IUPAC: ligands first (tetraammine), then metal with oxidation state [tetraamminecopper(II)]"},

  {"id":"NEET_CHE_003","exam":"NEET","subject":"Chemistry","topic":"Organic Chemistry","difficulty":"medium",
   "question":"Which of the following is NOT an isomer of C₄H₁₀?",
   "options":{"A":"n-Butane","B":"Isobutane","C":"Cyclobutane","D":"2-Methylpropane"},"answer":"C",
   "explanation":"Cyclobutane has formula C₄H₈ (cycloalkane), not C₄H₁₀. n-Butane and isobutane are both C₄H₁₀"},

  # ─── NEET BIOLOGY ──────────────────────────────────────────────────────────
  {"id":"NEET_BIO_001","exam":"NEET","subject":"Biology","topic":"Cell Biology","difficulty":"easy",
   "question":"The powerhouse of the cell is:",
   "options":{"A":"Nucleus","B":"Ribosome","C":"Mitochondria","D":"Golgi apparatus"},"answer":"C",
   "explanation":"Mitochondria produce ATP via cellular respiration, hence called the powerhouse of the cell"},

  {"id":"NEET_BIO_002","exam":"NEET","subject":"Biology","topic":"Genetics","difficulty":"medium",
   "question":"If both parents are Aa, the probability of offspring being aa is:",
   "options":{"A":"1/4","B":"1/2","C":"3/4","D":"1"},"answer":"A",
   "explanation":"Aa × Aa → AA:Aa:aa = 1:2:1. Probability of aa = 1/4"},

  {"id":"NEET_BIO_003","exam":"NEET","subject":"Biology","topic":"Human Physiology","difficulty":"medium",
   "question":"The enzyme responsible for the conversion of fibrinogen to fibrin in blood clotting is:",
   "options":{"A":"Pepsin","B":"Thrombin","C":"Trypsin","D":"Lipase"},"answer":"B",
   "explanation":"Thrombin converts soluble fibrinogen to insoluble fibrin mesh during blood clotting"},

  {"id":"NEET_BIO_004","exam":"NEET","subject":"Biology","topic":"Plant Physiology","difficulty":"medium",
   "question":"Photosynthesis occurs in:",
   "options":{"A":"Mitochondria","B":"Nucleus","C":"Chloroplast","D":"Ribosome"},"answer":"C",
   "explanation":"Chloroplasts contain chlorophyll and are the sites of photosynthesis in plant cells"},

  {"id":"NEET_BIO_005","exam":"NEET","subject":"Biology","topic":"Evolution","difficulty":"easy",
   "question":"The theory of Natural Selection was proposed by:",
   "options":{"A":"Lamarck","B":"Mendel","C":"Darwin","D":"Watson"},"answer":"C",
   "explanation":"Charles Darwin proposed the theory of evolution by natural selection in 'On the Origin of Species' (1859)"},

  {"id":"NEET_BIO_006","exam":"NEET","subject":"Biology","topic":"Ecology","difficulty":"medium",
   "question":"Pyramid of energy is always:",
   "options":{"A":"Inverted","B":"Upright","C":"Spindle shaped","D":"Both A and B"},"answer":"B",
   "explanation":"Energy decreases at each trophic level (only 10% transferred), so energy pyramid is always upright"},

  {"id":"NEET_BIO_007","exam":"NEET","subject":"Biology","topic":"Reproduction","difficulty":"easy",
   "question":"Double fertilization is a characteristic of:",
   "options":{"A":"Gymnosperms","B":"Angiosperms","C":"Algae","D":"Fungi"},"answer":"B",
   "explanation":"Double fertilization (one egg + one sperm; one central cell + one sperm) is unique to angiosperms"},

  # ─── GATE CS ───────────────────────────────────────────────────────────────
  {"id":"GATE_CS_001","exam":"GATE","subject":"Computer Science","topic":"Data Structures","difficulty":"medium",
   "question":"What is the time complexity of binary search on a sorted array of n elements?",
   "options":{"A":"O(n)","B":"O(n²)","C":"O(log n)","D":"O(n log n)"},"answer":"C",
   "explanation":"Binary search halves the search space each step → T(n) = T(n/2) + O(1) → O(log n)"},

  {"id":"GATE_CS_002","exam":"GATE","subject":"Computer Science","topic":"Algorithms","difficulty":"hard",
   "question":"Which sorting algorithm has the best worst-case time complexity?",
   "options":{"A":"Quick Sort","B":"Bubble Sort","C":"Merge Sort","D":"Selection Sort"},"answer":"C",
   "explanation":"Merge Sort always runs in O(n log n) even in worst case. Quick Sort worst case is O(n²)"},

  {"id":"GATE_CS_003","exam":"GATE","subject":"Computer Science","topic":"Operating Systems","difficulty":"medium",
   "question":"Deadlock cannot occur if which condition is NOT satisfied?",
   "options":{"A":"Mutual Exclusion","B":"Hold and Wait","C":"No Preemption","D":"All of the above"},
   "answer":"D","explanation":"All 4 Coffman conditions (Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait) must hold for deadlock"},

  {"id":"GATE_CS_004","exam":"GATE","subject":"Computer Science","topic":"Database","difficulty":"medium",
   "question":"Which normal form eliminates transitive dependencies?",
   "options":{"A":"1NF","B":"2NF","C":"3NF","D":"BCNF"},"answer":"C",
   "explanation":"Third Normal Form (3NF) eliminates transitive functional dependencies (non-key → non-key)"},

  {"id":"GATE_CS_005","exam":"GATE","subject":"Computer Science","topic":"Networks","difficulty":"easy",
   "question":"The protocol used to convert IP address to MAC address is:",
   "options":{"A":"DNS","B":"DHCP","C":"ARP","D":"RARP"},"answer":"C",
   "explanation":"ARP (Address Resolution Protocol) maps IP addresses to MAC (physical) addresses"},

  {"id":"GATE_CS_006","exam":"GATE","subject":"Computer Science","topic":"Theory of Computation","difficulty":"hard",
   "question":"Which of the following is not a context-free language?",
   "options":{"A":"aⁿbⁿ | n≥0","B":"Palindromes","C":"aⁿbⁿcⁿ | n≥0","D":"Regular expressions"},"answer":"C",
   "explanation":"aⁿbⁿcⁿ requires counting 3 symbols simultaneously — beyond CFL power, requires CSL"},

  {"id":"GATE_CS_007","exam":"GATE","subject":"Computer Science","topic":"Computer Architecture","difficulty":"medium",
   "question":"In cache memory, the concept of locality means:",
   "options":{"A":"Programs access random memory","B":"Recently accessed data is likely accessed again",
               "C":"Cache is always full","D":"Main memory is slow"},"answer":"B",
   "explanation":"Locality of reference: spatial (nearby addresses) and temporal (recently used data accessed again soon)"},

  # ─── GATE ECE ───────────────────────────────────────────────────────────────
  {"id":"GATE_ECE_001","exam":"GATE","subject":"Electronics","topic":"Signals & Systems","difficulty":"medium",
   "question":"The Fourier transform of a unit impulse function δ(t) is:",
   "options":{"A":"0","B":"1","C":"jω","D":"1/jω"},"answer":"B",
   "explanation":"F{δ(t)} = ∫δ(t)e^(-jωt)dt = e^0 = 1. The spectrum is flat (white spectrum)"},

  {"id":"GATE_ECE_002","exam":"GATE","subject":"Electronics","topic":"Digital Circuits","difficulty":"easy",
   "question":"The Boolean expression A·Ā is equal to:",
   "options":{"A":"A","B":"Ā","C":"1","D":"0"},"answer":"D",
   "explanation":"Complement law: A·Ā = 0 (AND of a variable with its complement is always 0)"},

  # ─── UPSC GS ───────────────────────────────────────────────────────────────
  {"id":"UPSC_GS_001","exam":"UPSC","subject":"General Studies","topic":"Polity","difficulty":"medium",
   "question":"The Constitution of India was adopted on:",
   "options":{"A":"15 August 1947","B":"26 January 1950","C":"26 November 1949","D":"26 January 1949"},
   "answer":"C","explanation":"The Constitution was adopted on 26 November 1949 (Constitution Day) and came into force on 26 January 1950"},

  {"id":"UPSC_GS_002","exam":"UPSC","subject":"General Studies","topic":"History","difficulty":"easy",
   "question":"The first Governor-General of independent India was:",
   "options":{"A":"Rajendra Prasad","B":"Lord Mountbatten","C":"C. Rajagopalachari","D":"Jawaharlal Nehru"},
   "answer":"B","explanation":"Lord Mountbatten was the first Governor-General of independent India (1947–1948)"},

  {"id":"UPSC_GS_003","exam":"UPSC","subject":"General Studies","topic":"Geography","difficulty":"medium",
   "question":"The Tropic of Cancer passes through how many Indian states?",
   "options":{"A":"6","B":"7","C":"8","D":"9"},"answer":"C",
   "explanation":"Tropic of Cancer passes through 8 Indian states: Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, West Bengal, Tripura, Mizoram"},

  {"id":"UPSC_GS_004","exam":"UPSC","subject":"General Studies","topic":"Economy","difficulty":"medium",
   "question":"GDP at factor cost = GDP at market prices MINUS:",
   "options":{"A":"Net indirect taxes","B":"Subsidies","C":"Depreciation","D":"Transfer payments"},"answer":"A",
   "explanation":"GDP at FC = GDP at MP − Net indirect taxes (Indirect taxes − Subsidies)"},

  # ─── CAT ────────────────────────────────────────────────────────────────────
  {"id":"CAT_QA_001","exam":"CAT","subject":"Quantitative Aptitude","topic":"Number System","difficulty":"medium",
   "question":"The LCM of 12, 15 and 20 is:",
   "options":{"A":"60","B":"120","C":"180","D":"240"},"answer":"A",
   "explanation":"12 = 2²×3, 15 = 3×5, 20 = 2²×5. LCM = 2²×3×5 = 60"},

  {"id":"CAT_QA_002","exam":"CAT","subject":"Quantitative Aptitude","topic":"Percentages","difficulty":"medium",
   "question":"A shopkeeper sells goods at 20% profit. If the cost price is ₹500, the selling price is:",
   "options":{"A":"₹550","B":"₹580","C":"₹600","D":"₹620"},"answer":"C",
   "explanation":"SP = CP × (1 + profit%) = 500 × 1.20 = ₹600"},

  {"id":"CAT_VA_001","exam":"CAT","subject":"Verbal Ability","topic":"Reading Comprehension","difficulty":"medium",
   "question":"The word 'Ephemeral' most closely means:",
   "options":{"A":"Eternal","B":"Short-lived","C":"Powerful","D":"Mysterious"},"answer":"B",
   "explanation":"Ephemeral means lasting for a very short time, transitory, fleeting"},

  {"id":"CAT_LRDI_001","exam":"CAT","subject":"LRDI","topic":"Logical Reasoning","difficulty":"hard",
   "question":"If A > B, B > C, and C > D, then which is definitely true?",
   "options":{"A":"A > D","B":"D > A","C":"B > D only","D":"Cannot determine"},"answer":"A",
   "explanation":"By transitivity: A>B>C>D → A>D is definitely true"},
]

def get_questions_by_exam(exam: str, limit: int = 20) -> list:
    """Get questions filtered by exam name."""
    qs = [q for q in QUESTIONS if q["exam"].upper() == exam.upper()]
    return qs[:limit]

def get_questions_by_subject(exam: str, subject: str) -> list:
    """Get questions filtered by exam and subject."""
    return [q for q in QUESTIONS
            if q["exam"].upper() == exam.upper()
            and q["subject"].lower() == subject.lower()]

def get_all_exams() -> list:
    """Return list of unique exam names."""
    return sorted(list(set(q["exam"] for q in QUESTIONS)))

def get_subjects_for_exam(exam: str) -> list:
    """Return subjects available for a given exam."""
    return sorted(list(set(q["subject"] for q in QUESTIONS if q["exam"].upper() == exam.upper())))

def get_topics_for_subject(exam: str, subject: str) -> list:
    return sorted(list(set(
        q["topic"] for q in QUESTIONS
        if q["exam"].upper() == exam.upper() and q["subject"].lower() == subject.lower()
    )))
