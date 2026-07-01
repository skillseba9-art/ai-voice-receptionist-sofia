# 📋 Unified Restaurant Knowledge Base & AI Configuration Sheet

**Project:** Premium AI Voice Receptionist Implementation
**Target Location:** Dhanmondi, Dhaka, Bangladesh  
**Target Market Context:** High-End Local Fine Dining & Fusion Steakhouse

---

## 1. Restaurant Overview, Identity & Branding

* **Restaurant Name:** The Crimson Courtyard (Premium Fusion & Steakhouse)
* **Address:** House 42, Road 11A, Dhanmondi, Dhaka 1209 (Near Dhanmondi Lake)
  * *Google Maps Link:* `https://maps.google.com/?cid=mock_crimson_courtyard_dhanmondi`
* **Primary Inbound Phone Number:** +880 1711-XXXXXX (Receives forwarded calls via Twilio BYOC)
* **Email Address:** `reservations@crimsoncourtyard.com` (Used by n8n to send automated booking confirmations and post-call summaries)
* **Official Website:** `https://www.crimsoncourtyard.com` (AI will refer callers here for the interactive layout and photo galleries)
* **Social Media Handles:**
  * *Facebook:* `fb.com/CrimsonCourtyardDhanmondi`
  * *Instagram:* `@CrimsonCourtyard.Dhaka`
* **Tagline:** *"Where Steak Meets Elegance"*
* **Ambiance / Vibe:** Premium, sophisticated, and intimate fine dining featuring an outdoor lakeside view terrace. It is highly optimized for romantic dinners, upscale family gatherings, and corporate executive meetings. It is **not** styled as a high-volume wedding reception hall, but it perfectly accommodates private anniversary parties and corporate dinners.
* **Operating Hours:**
  * *Sunday to Thursday:* 12:00 PM – 11:00 PM
  * *Friday & Saturday:* 12:00 PM – 11:30 PM

---

## 2. Menu, Kitchen Logic & Dietary Customizations

* **Menu Layout:** Full dynamic data is managed inside Google Sheets. The core high-traffic categories are:
  * *Appetizers:* Peri Peri Chicken Wings (BDT 700), Cream of Mushroom Soup (BDT 600).
  * *Signature Steaks:* Ribeye Steak (BDT 2,600), T-Bone Steak (BDT 2,950).
  * *Platters:* Seafood Platter (BDT 3,500), Courtyard Special Mix Platter (BDT 3,300).
  * *Mocktails & Desserts:* Mint Lemonade (BDT 350), Sizzling Brownie with Ice Cream (BDT 600).
* **Steak-Specific Logic:** The AI agent **must** ask the caller for their preferred level of doneness: *Rare, Medium Rare, Medium, or Well Done*.
* **Hero Items for Upselling:** When asked for a recommendation, the agent must pitch the *Signature Ribeye Steak* or the *Courtyard Special Mix Platter*.
* **Dietary & Allergen Restrictions:**
  * *Vegetarian/Vegan Options:* Mushroom Risotto (BDT 1,200) and Grilled Vegetable Medley (BDT 950).
  * *Kids Menu:* Mini Chicken Sliders with Fries (BDT 550), Mac & Cheese Junior (BDT 600). Portions are downsized specifically for children under 10.
  * *Allergen Warnings:* The Cream of Mushroom Soup contains dairy and gluten. The Peri Peri Wings contain trace amounts of peanut oil. The agent must warn customers explicitly if they mention a peanut, dairy, or gluten allergy.
  * *Healthy/Low-Carb Options:* Steaks can be ordered with a double side of sautéed asparagus and broccoli instead of mashed potatoes/fries for a Keto/low-carb profile.
* **Preparation & Lead Times:**
  * Steaks and Platters require a **25–30 minute** kitchen lead time.
  * Appetizers and Mocktails take **10–12 minutes**.
  * The agent must inform callers ordering ahead or booking a tight slot about these times.
* **Kitchen Customization:** Customers can request spicy levels (*Mild, Medium, Hot*) for the Peri Peri Wings and pasta dishes. Pasta noodle variants (Fettuccine vs. Penne) cannot be customized over the phone.
* **Daily Specials:** The restaurant does not run arbitrary daily specials; instead, the *Seafood Platter* depends on the daily catch. If reserved, the agent tags the reservation payload as `[Seafood Requested]`.

---

## 3. Booking, Seating Configurations & Reservation Policies

* **Advance Booking Window:** Reservations can be placed up to 14 days in advance.
* **Minimum Booking Notice:** Bookings must be registered at least 1 hour before arrival.
* **Seating Architecture & Configuration:**
  * Total capacity: 22 Tables.
  * *2-Seater Tables:* 8 tables (ideal for couples).
  * *4-Seater Tables:* 8 tables (standard family/business setups).
  * *6-Seater Tables:* 4 tables.
  * *8-Seater Tables:* 2 tables.
* **Premium Seating (Lakeside View):** 2 exclusive Lakeside View tables are available. They carry a minimum spend condition of **BDT 4,000**. The agent will pitch this option for special occasions or romantic reservations.
* **Large Group Policy (10+ Guests):**
  * Requires a mandatory advance deposit of **BDT 5,000** to secure the floor space.
  * The agent **cannot** auto-confirm reservations exceeding 10 guests. It must collect the customer's details and execute a warm transfer to management or state: *"Our manager will contact you via phone within 15 minutes to confirm your deposit details."*
* **Deposit Payment Channels:** The BDT 5,000 large group deposit must be sent via **bKash Merchant Account Number: +880 1799-XXXXXX** (Reference: Customer Phone Number). Alternatively, walk-in cash or physical card swipes at the desk are accepted within 24 hours of booking.
* **Walk-In & No-Show Policies:**
  * Reservations are held for a maximum grace period of **20 minutes** past the slot before the table is released to walk-ins.
  * There is no financial penalty or automated charge for a cancellation or no-show, but a 1-hour cancellation notice via phone is strongly requested.
  * *Walk-in Waiting Times:* During peak hours (Friday/Saturday night), walk-in guests face an average wait time of 30 to 45 minutes.
* **Confirmation & Reminder Automations:**
  * *Channel:* Handled dynamically via n8n. Upon successful booking, a structured SMS is fired to the user via Twilio, and a confirmation email is dispatched.
  * *Reminders:* An automated SMS reminder is pushed via n8n exactly **3 hours prior** to the reservation time to minimize no-shows.

---

## 4. Delivery, Takeaway & Logistics

* **In-House Fleet:** The Crimson Courtyard does **not** operate a proprietary delivery fleet.
* **Third-Party Platforms:** Listed exclusively on **Foodpanda** and **Pathao Food**.
  * *Direct Links:* Provided via automated SMS if requested (`foodpanda.com/re/crimsoncourtyard` or `pathao.com/food/crimson-courtyard`).
  * *Order Cutoff Time:* Third-party delivery orders are shut down at **10:30 PM** daily, 30 minutes before the physical restaurant closes.
* **Takeaway / Self-Pickup:** Fully supported. Customers can call ahead to place a takeaway order. The agent will process the order, write it to Google Sheets, collect their phone number, and state: *"Your order will be packed and ready for pickup at our front desk in 25 minutes."*
* **Catering Services:** The restaurant offers premium off-site catering for corporate events and high-end private parties (minimum 30 guests). The voice agent will capture catering leads (Name, Phone, Guest Count, Date) and route them to the catering manager's sheet for a callback.

---

## 5. Billing, Taxes & Payment Framework

* **Accepted Methods:** Cash (BDT), Visa, Mastercard, American Express (Amex), bKash, and Nagad.
* **Taxes and Surcharges:**
  * All printed menu prices are subject to a **10% Service Charge** and a **15% Government VAT** added to the final bill.
  * There are no additional surcharges or convenience fees for credit cards or mobile financial services (bKash/Nagad).
* **Discounts:** No flat cash-payment discounts are offered. Ongoing 1+1 (Buy One Get One) privileges apply strictly to premium credit cards from Eastern Bank Ltd (EBL), City Bank Amex, and Standard Chartered Bank (SCB). Card eligibility must be verified by the waiter at the billing counter.
* **Tipping / Gratuity:** Left completely to the guest's discretion. Tipping can be paid in cash directly to the service staff or added manually into the card machine during payment processing.

---

## 6. Frequently Asked Questions (FAQ Knowledge Base)

* **Q: Is there a specific dress code?**
  * *A:* Smart casual. Gym wear, singlets, tank tops, and open rubber flip-flops are prohibited inside the main dining hall.
* **Q: Do you have baby high chairs?**
  * *A:* Yes, multiple baby high chairs are available on-demand for family dining comfort.
* **Q: Can I bring an external birthday or anniversary cake?**
  * *A:* Yes. A minimal cake-cutting and service fee of **BDT 500** applies. Alternatively, you can pre-order a custom pastry from our in-house chef 24 hours in advance.
* **Q: Do you allow outside food or drinks?**
  * *A:* Outside food and beverages are strictly prohibited.
* **Q: Is there a private lounge or room for corporate meetings?**
  * *A:* Yes, a Private Dining Room (PDR) is available for up to 16 guests. It requires a minimum billing threshold of **BDT 15,000**.
* **Q: Do you provide complementary Wi-Fi?**
  * *A:* Yes. Network: `Crimson_Guest` | Password: `steakandelegance`.
* **Q: Is there live music or entertainment?**
  * *A:* Yes, acoustic live jazz performances occur every Friday night from 7:30 PM to 10:00 PM on the outdoor terrace. No extra entry charge applies.
* **Q: Is the venue accessible for individuals using wheelchairs?**
  * *A:* Fully accessible. We feature an entry ramp at the ground floor foyer, spacious elevator routing, and a dedicated accessible restroom facility on the main dining floor.
* **Q: Are pets allowed (Pet-Friendly policy)?**
  * *A:* Out of respect for family dining comfort and local hygienic regulations, pets are strictly prohibited inside both the indoor hall and outdoor terrace.
* **Q: Is there a dedicated kids play area?**
  * *A:* No separate play zone or playground is available. Children must remain seated with their families.

---

## 7. Operational Constraints & Escalation Architecture

* **Friday Prayer Break:** The restaurant pauses all operations on Fridays from **12:30 PM to 2:15 PM** for Jumm'ah prayers. The kitchen is paused, and the agent must explicitly reject or block booking intervals falling within this window.
* **Alcohol & Smoking Policy:**
  * The restaurant is a 100% alcohol-free, family-centric establishment. Alcohol is prohibited.
  * Smoking is banned inside the main air-conditioned dining hall. A designated smoking zone is located on the open-air terrace.
* **Escalation Protocols (Warm Transfer):**
  * If a customer calls to voice a complaint about a past order, requests financial refunds, or demands an immediate conversation with the owner, the AI must instantly perform a warm transfer to the **Manager's Handset: +880 1711-YYYYYY**.
  * *Backup Staff Contact:* If the primary manager line fails to connect, the agent routes to the assistant supervisor at **+880 1711-ZZZZZZ**.
* **After-Hours Infrastructure:**
  * If a call arrives outside operational timelines, Retell AI triggers an after-hours greeting: *"Thank you for calling The Crimson Courtyard. We are currently closed. Please state your name, phone number, and reservation request after the tone, and our team will contact you tomorrow morning after 12:00 PM."*
  * *n8n Data Sink:* The recorded voicemail URL, caller ID, and transcription are captured via an n8n webhook and saved immediately to a **Centralized Google Sheet (`After_Hours_Leads`)** while firing a priority Slack notification to the management group.

---

## 8. Technical & Voice System Specifications

* **Call Volume Target:** Expected traffic averages **80 to 120 calls per day**. Server scaling and Retell concurrent call paths are provisioned to handle up to 5 concurrent sessions smoothly.
* **Peak Traffic Window:** High-density calling occurs daily between **6:00 PM and 9:00 PM**. The n8n automation worker polling timeout values are tuned higher during this phase to avoid concurrency drops.
* **Call Recording & Retention:** All voice calls are recorded for service evaluation and logging. Audio streams and transcript objects are retained securely inside Retell AI and mirrored to our cloud storage bucket for **90 days**, after which they are auto-purged to respect privacy guidelines.
* **Voice Personality Design:** The ElevenLabs Flash voice profile is configured to sound **Warm, Professional, Clear, and Welcoming**, mirroring a high-end luxury hospitality receptionist. It maintains a calm cadence even when handling fast or repetitive speech patterns.
* **Language & Accent Preference:** **Pure English**. The agent speaks, responds, and logs variables completely in clear English. However, it is explicitly injected with a localized custom lexicon to seamlessly comprehend Bangladeshi english accents, names, and localized terms (such as *Dhanmondi, bKash, Jumm'ah, Nagad, Pathao, or Takas*) without breaking script execution or dropping context.
