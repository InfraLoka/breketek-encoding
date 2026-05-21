What happens when the law cannot parse the message? Two interpretive edge cases — foreign-language ambiguity and cross-thread encryption — that expose a critical gap in Indonesia's electronic information law.

A law is only as strong as its ability to be consistently interpreted. UU ITE — Indonesia's Electronic Information and Transactions Law — was written for a world that is increasingly speaking in many languages, encrypting its messages, and distributing meaning across platforms. The law has not fully caught up.

I want to talk about two specific scenarios that I believe represent genuine legal "bugs" — not in the code, but in the statute itself. Situations where the law's plain text fails to produce a deterministic outcome because the meaning of the alleged offense depends on interpretive machinery the law does not formally provide.

These are not hypothetical edge cases invented in a law school classroom. They are practical problems that will — and likely already do — arise in real prosecutions and civil disputes under UU ITE. And until they are addressed, they create asymmetric risk: the accused bears the uncertainty, while the law pretends clarity it does not have.

The Framework: What UU ITE Prohibits
The core provisions most frequently invoked in online speech cases are found in Pasal 27 and Pasal 28 of UU ITE No. 19 Tahun 2016, as amended by UU No. 1 Tahun 2024. The law prohibits, among other things, distributing electronic content that is considered defamatory (pencemaran nama baik), threatening, indecent, or producing enmity based on group identity (SARA).

UU ITE Pasal 27 Ayat (3) — Pencemaran Nama BaikSetiap Orang dengan sengaja dan tanpa hak mendistribusikan dan/atau mentransmisikan dan/atau membuat dapat diaksesnya Informasi Elektronik dan/atau Dokumen Elektronik yang memiliki muatan penghinaan dan/atau pencemaran nama baik.

The key operative phrase is "memiliki muatan" — "has the content of." The law asks: does this electronic information have the content of defamation, threat, or obscenity? This is a semantic question. And semantics, it turns out, is where the bugs live.

Bug #1 — The Foreign Language Problem
Bug Report · #ITE-001

When the Alleged Offense Speaks a Language the Law Does Not

Scenario: A message is sent in Javanese slang, Minang dialect, Hokkien-influenced Indonesian, or in standard English, Dutch, Arabic, or Korean — languages with no authoritative entry in the Kamus Besar Bahasa Indonesia (KBBI). The prosecution alleges the message is defamatory or threatening. The defense disputes the meaning of the key term. Who decides?

This is not a trivial problem. Indonesia is home to over 700 regional languages and dialects, and its digital public sphere is profoundly multilingual. WhatsApp group chats, Twitter/X threads, and Instagram comments routinely mix Indonesian with Javanese, Sundanese, Betawi, Batak, Makassarese — and increasingly with Korean, Arabic, or English terms adopted into informal Indonesian usage.

UU ITE says nothing about the language in which electronic content must be evaluated. It does not designate the KBBI as the authoritative lexicon for determining meaning. It does not require linguistic expert testimony. It leaves the question of semantic interpretation almost entirely open.

The Concrete Risk
Consider a message that uses a Javanese word — say, a term of casual insult between friends in a regional dialect — that has no direct Indonesian equivalent. A judge or investigator unfamiliar with that dialect may assign a meaning to the term that differs substantially from its actual communicative intent. The accused faces conviction not for what they said, but for what the law imagined they said.

Hypothetical Scenario · Group Chat

[User A]: Wah si B tuh mbok ya "nggapleki" banget!

[Investigator reads as]: Severe personal insult → Pasal 27(3)

[Linguist testifies]: Colloquial Javanese expression of mild frustration, contextually equivalent to "oh come on" — not defamatory in register or intent

[Question]: Which reading does the law require?

Or consider the inverse: a message written in formal English that uses a technical or legal term which, if read literally by a non-English speaker, appears threatening — but in its proper professional context is standard industry language. The absence of a KBBI entry for the disputed term means there is no official semantic anchor.

"The law prohibits content that 'has the meaning of' an offense. But it does not specify whose reading of that meaning controls — and that gap is a due process problem."

Why Linguistic Expert Testimony Must Be Mandatory
In systems like the United States or the Netherlands, courts routinely appoint linguistic experts (ahli bahasa) in defamation cases where the meaning of a word or phrase is genuinely disputed. In Indonesia, the use of such experts is permitted under KUHAP but is not mandated by UU ITE for any category of case.

This creates an asymmetry. Prosecutors can assert meaning. Defendants can dispute it. But without a formal requirement for linguistic expert testimony when a term falls outside KBBI — or when the message is in a regional language — the factual determination of "what this message means" is left to the unaided interpretation of investigators and judges who may lack the competence to make that call accurately.

Language CategoryKBBI CoverageRisk LevelExpert Required?Standard Indonesian (formal)CompleteLowRarelyIndonesian slang / gaulPartialMediumSometimesRegional dialects (Javanese, Sundanese, etc.)MinimalHighNot mandated by lawForeign language (English, Arabic, Korean)NoneHighNot mandated by lawMixed-language / code-switchingNoneCriticalNot mandated by law

Bug #2 — The Split-Key Encryption Problem
Bug Report · #ITE-002

When the Message and Its Meaning Live in Different Places

Scenario: An encrypted or encoded message is posted in one thread, platform, or public space. The decryption key — or the context that gives the cipher its meaning — exists in a separate thread, a different platform, or a prior communication that may no longer be accessible. Prosecutors allege the decoded message violates UU ITE. Defense argues the message, as received by any ordinary reader, is meaningless. Who bears the burden of proving what the message "means"?

This scenario is more sophisticated, but it is not science fiction. It already happens — in coded language communities, in activist networks that use substitution ciphers shared in separate channels, in corporate communications using internal jargon whose key is a handbook published elsewhere, and in the growing use of steganography and simple encryption by ordinary citizens who want private communication.

The Legal Architecture Problem
UU ITE defines "Informasi Elektronik" broadly as any electronic data in a form that can be processed, stored, transferred, and displayed. It does not distinguish between a message that is immediately legible to its recipients and one that requires additional information — a key, a codebook, a separate document — to decode.

The law asks: does this information "have the content of" an offense? But if the information is encrypted, it has no legible content without the key. The question of whether it constitutes illegal content therefore cannot be answered without first establishing: (a) that a key exists, (b) where that key is located, (c) that the key actually decodes the message into the alleged offensive content, and (d) that the sender intended the decoding to occur in the way the prosecution alleges.

Thread A — Public Forum Post

[User A posts]: Jg17#KLm → X3q9%Brt → Pz44@nN2

Thread B — Separate Private Group (deleted):

[Key shared earlier]: Cipher: J=A, g=n, 1=t, 7=a, # = space... [ROT-based substitution]

[Decoded per prosecution]: Alleged defamatory statement about [Party X]

[Question]: Was Thread A's post "distributing defamatory electronic information" at the moment of posting? Or only upon decoding — if ever decoded?

Three Unresolved Questions the Law Cannot Answer
UU ITE provides no guidance on any of the following:

1. Chain of custody for the key. If the decryption key was shared in a now-deleted thread or a platform outside Indonesian jurisdiction, how does the prosecution establish that the key is authentic and was actually used by the recipient to read the alleged offense? If the key cannot be produced, can the prosecution reconstruct the meaning through cryptanalysis? Is that reconstruction admissible?

2. The moment of offense. Defamation, under Indonesian civil and criminal law, requires that the harmful content reach an audience — it must be received, read, understood. If an encrypted message is distributed but no recipient possesses the key, has an offense occurred? The law's use of the phrase "dapat diaksesnya" — "can be accessed" — suggests the information must be accessible. But accessible to whom, with what tools?

3. Multi-hop meaning. What if the key itself requires a prior key? What if the offensive meaning only emerges after three layers of decoding, each stored in a different location? At what point does the chain of inference become too speculative to sustain a conviction?

"If meaning is distributed across platforms and threads, then no single post 'has the content of' an offense — and the law must confront what it means to prosecute a message that cannot stand alone."

The Comparison: How Other Frameworks Handle This
The EU's Digital Services Act and existing European cybercrime frameworks under the Budapest Convention address encrypted content by requiring that prosecution establish both the existence of the key and the chain of access — placing the evidentiary burden clearly on the state. The United States' approach under the Electronic Communications Privacy Act similarly requires warrants that specify what is being sought and for what decryption. These frameworks acknowledge that encryption is not a legal magic trick — it changes what the "content" of a communication is, and the law must adapt.

UU ITE does not have an equivalent provision. It treats an encrypted blob and a plaintext defamatory post as equivalent categories of "Informasi Elektronik." That equivalence is the bug.

Why These Bugs Are Not Minor
Someone reading this might argue: courts are routinely asked to interpret meaning. Judges handle ambiguity all the time. Why should these cases be different?

The answer is that ordinary interpretive ambiguity operates within a shared semantic system — both parties speak the same language, use the same dictionary, operate in the same communicative context. The two bugs I have described operate outside that shared system. They require the court to make determinations about meaning that require specialized expertise (linguistics, cryptography) that is not currently mandated by law, and that most Indonesian courts — especially at the district level — are not equipped to evaluate independently.

In a country where UU ITE has historically been used asymmetrically — more often against critics, journalists, activists, and ordinary citizens than against those with institutional power — interpretive ambiguity is not a neutral technical problem. It is a structural advantage for whoever initiates the prosecution. The burden of explaining what a word means, or why a decoded message is or is not what the prosecution claims, falls on the accused. And that burden, in practice, can be crushing.

Toward a Fix: What Reformed UU ITE Should Include
A mandatory provision requiring ahli bahasa (linguistic expert) testimony whenever the disputed content contains terms not found in KBBI or is written in a language other than standard Indonesian — with the cost of such testimony borne by the state in criminal proceedings.

A definition of "accessible electronic information" that explicitly addresses encrypted content — distinguishing between information that is accessible to ordinary recipients and information that requires additional keys, context, or technical capability to decode.

A chain-of-custody standard for decryption keys used as evidence, requiring that the prosecution establish the authenticity of the key, the method of decryption, and the identity of parties who possessed both the message and the key simultaneously.

An explicit standard for cross-platform evidence— addressing situations where the meaning of a post on one platform depends on content located on another platform, especially one outside Indonesian jurisdiction or that has since been deleted.

Formal recognition that semantic determination is a factual question requiring expert input, not a legal question resolvable by judicial notice — and that a judge's personal reading of an unfamiliar term or decoded cipher does not constitute sufficient factual finding.

Closing: The Law Must Be Able to Parse What It Polices
Indonesia's digital economy is growing at a pace that UU ITE, even in its 2024 amended form, is struggling to match. The law was designed for a simpler information environment — one where messages were written in clear Indonesian, sent from one person to another, and readable without additional context.

That environment no longer exists. We communicate across languages, across platforms, across encryption layers. We speak in memes, in coded references, in dialects that have no KBBI entry. We distribute context across time and space in ways that make any single message, read in isolation, an incomplete artifact.

A law that cannot account for this reality will be applied inconsistently. And inconsistent application of a criminal statute — especially one with the reach and history of UU ITE — is not a neutral outcome. It means that some people will be prosecuted for messages that were lawful, and some will escape accountability for messages that were harmful, based on nothing more principled than interpretive luck.

These bugs need to be filed. Formally, loudly, and soon.

I write at the intersection of technology, law, and Indonesia's digital future. If you are working on UU ITE reform, digital rights advocacy, or legal technology in Southeast Asia — I would welcome the conversation.

#UUITE #DigitalLaw #Indonesia #CyberLaw #LegalTech #HakDigital #Linguistik #Enkripsi #Infraloka

This article reflects the author's independent legal analysis and does not constitute legal advice. For specific legal matters, consult a qualified advocate or LBH.