/**
 * Iga EdTech — Internationalisation (i18n)
 * EN ↔ RW for every page.
 *
 * HOW TO ADD A NEW STRING:
 *   1. Add an entry:  "my.key": { en: "Hello", rw: "Muraho" }
 *   2. Add the attribute to HTML: data-i18n="my.key"
 *   3. For inputs: data-i18n-placeholder="my.key"
 *   4. In JS code: t('my.key')
 *   No page reload needed during dev — call applyLang() in the console.
 */

const TRANSLATIONS = {

  // ══════════════════════════════════════════════════════════════
  //  NAVBAR
  // ══════════════════════════════════════════════════════════════
  "role.teacher":      { en: "Teacher",             rw: "Umwarimu" },
  "role.student":      { en: "Student",             rw: "Umunyeshuri" },
  "role.admin":        { en: "Admin",               rw: "Umuyobozi" },
  "topbar.logout":     { en: "Logout",              rw: "Sohoka" },
  "nav.login":         { en: "Login",              rw: "Injira" },
  "nav.signup":        { en: "Sign Up",             rw: "Iyandikishe" },
  "nav.journey":       { en: "Start the journey",   rw: "Tangira Urugendo" },

  // ══════════════════════════════════════════════════════════════
  //  FOOTER
  // ══════════════════════════════════════════════════════════════
  "footer.learn":      { en: "Learn",               rw: "Kwiga" },
  "footer.courses":    { en: "Courses",              rw: "Amasomo" },
  "footer.assessment": { en: "Assessment",           rw: "Ikizamini" },
  "footer.contact":    { en: "Contact Us On",        rw: "Twandikire" },
  "footer.terms":      { en: "Terms",                rw: "Amategeko" },
  "footer.privacy":    { en: "Privacy Policy",       rw: "Amabwiriza y'Ibanga" },
  "footer.socials":    { en: "Socials",              rw: "Imbuga" },
  "footer.rights":     { en: "© 2026 Iga EdTech || All rights reserved.", rw: "© 2026 Iga EdTech || Uburenganzira bwose burubahirizwa." },

  // ══════════════════════════════════════════════════════════════
  //  HOMEPAGE
  // ══════════════════════════════════════════════════════════════
  "home.hero.title":   { en: "Quality Education for Every Rwandan Learner", rw: "Uburezi Bwiza ku Banyarwanda Bose" },
  "home.hero.sub":     { en: "Access courses, assessments and learning materials in Kinyarwanda and English — anytime, anywhere.", rw: "Fata amasomo, ibizamini n'ibikoresho byo kwiga mu Kinyarwanda no mu Cyongereza — igihe cyose, ahantu hose." },
  "home.hero.cta1":    { en: "Start Learning →",    rw: "Tangira Kwiga →" },
  "home.hero.cta2":    { en: "Become a Teacher",    rw: "Ba Umwarimu" },
  "home.feat1.title":  { en: "Rich Course Library", rw: "Ububiko Bukungahaye bw'Amasomo" },
  "home.feat1.desc":   { en: "Access courses across Mathematics, Sciences, Languages and more — all designed for Rwandan learners.", rw: "Fata amasomo y'Imibare, Siyansi, Indimi n'ibindi — byose bigenewe abanyeshuri nyarwanda." },
  "home.feat2.title":  { en: "Assessments & Quizzes", rw: "Ibizamini n'Amasuzuma" },
  "home.feat2.desc":   { en: "Test your knowledge with quizzes and get instant feedback. Track your performance over time.", rw: "Gerageza ubumenyi bwawe ukoresheje ibibazo kandi ubone igisubizo vuba. Kurikirana aho ugeze igihe cyose." },
  "home.feat3.title":  { en: "Kinyarwanda & English", rw: "Ikinyarwanda n'Icyongereza" },
  "home.feat3.desc":   { en: "All content available in both Kinyarwanda and English so every student can learn in their preferred language.", rw: "Ibintu byose biboneka mu Kinyarwanda no mu Cyongereza kugira ngo buri munyeshuri yige mu rurimi rw'amahitamo." },

  // ══════════════════════════════════════════════════════════════
  //  AUTH — SHARED PLACEHOLDERS & LABELS
  // ══════════════════════════════════════════════════════════════
  "auth.email":        { en: "Email",               rw: "Imeyili" },
  "auth.password":     { en: "Password",            rw: "Ijambo ry'ibanga" },
  "auth.fullname":     { en: "Full Names",           rw: "Amazina Yombi" },
  "auth.forgot":       { en: "Forgot password?",    rw: "Wibagiwe ijambo ry'ibanga?" },

  // Student login placeholders
  "login.email":       { en: "Email",               rw: "Imeyili" },
  "login.password":    { en: "Password",            rw: "Ijambo ry'ibanga" },
  "login.forgot":      { en: "Forgot password?",    rw: "Wibagiwe ijambo ry'ibanga?" },

  // Student register placeholders
  "reg.fullname":      { en: "Full Names",           rw: "Amazina Yombi" },
  "reg.email":         { en: "Email",               rw: "Imeyili" },
  "reg.password":      { en: "Password",            rw: "Ijambo ry'ibanga" },

  // Teacher register placeholders
  "treg.fullname":     { en: "Full Names",           rw: "Amazina Yombi" },
  "treg.email":        { en: "Email",               rw: "Imeyili" },
  "treg.password":     { en: "Password",            rw: "Ijambo ry'ibanga" },
  "treg.dept":         { en: "Department (optional)", rw: "Ishami (si ngombwa)" },

  // OTP
  "otp.title":         { en: "Verify your email",   rw: "Emeza imeyili yawe" },
  "otp.sent":          { en: "We sent a 6-digit code to", rw: "Twohereje umubare w'imibare 6 kuri" },
  "otp.btn":           { en: "Verify Email",         rw: "Emeza Imeyili" },
  "otp.resend":        { en: "Didn't receive it?",   rw: "Ntiwabikeye?" },
  "otp.resendlink":    { en: "Resend code",          rw: "Ohereza kode bushya" },

  // ══════════════════════════════════════════════════════════════
  //  STUDENT LOGIN
  // ══════════════════════════════════════════════════════════════
  "login.title":       { en: "Log in to continue your e-learning journey", rw: "Injira wige" },
  "login.btn":         { en: "Login with email",    rw: "Injira ukoresheje imeyili" },
  "login.noaccount":   { en: "Don't have an account?", rw: "Nta konti ufite?" },
  "login.signup":      { en: "Sign up",             rw: "Iyandikishe" },
  "login.teacher":     { en: "Are you a teacher? Login here →", rw: "Uri umwarimu? Injira hano →" },

  // ══════════════════════════════════════════════════════════════
  //  TEACHER LOGIN
  // ══════════════════════════════════════════════════════════════
  "tlogin.title":      { en: "Login as a teacher",  rw: "Injira nk'umwarimu" },
  "tlogin.btn":        { en: "Login with email",    rw: "Injira ukoresheje imeyili" },
  "tlogin.noaccount":  { en: "Don't have an account?", rw: "Nta konti ufite?" },
  "tlogin.register":   { en: "Register",            rw: "Iyandikishe" },
  "tlogin.student":    { en: "← Student login",     rw: "← Injira nk'umunyeshuri" },

  // ══════════════════════════════════════════════════════════════
  //  STUDENT REGISTER
  // ══════════════════════════════════════════════════════════════
  "reg.title":         { en: "Sign up and start learning", rw: "Iyandikishe utangire kwiga" },
  "reg.btn":           { en: "Sign Up",             rw: "Iyandikishe" },
  "reg.hasaccount":    { en: "Already have an account?", rw: "Ufite konti?" },
  "reg.login":         { en: "Log in",              rw: "Injira" },
  "reg.teacher":       { en: "Are you a teacher? Register here →", rw: "Uri umwarimu? Iyandikishe hano →" },

  // ══════════════════════════════════════════════════════════════
  //  TEACHER REGISTER
  // ══════════════════════════════════════════════════════════════
  "treg.title":        { en: "Sign up as a teacher", rw: "Iyandikishe nk'umwarimu" },
  "treg.btn":          { en: "Sign Up",             rw: "Iyandikishe" },
  "treg.hasaccount":   { en: "Already have an account?", rw: "Usangiye konti?" },
  "treg.login":        { en: "Log in",              rw: "Injira" },

  // ══════════════════════════════════════════════════════════════
  //  STUDENT DASHBOARD — SIDEBAR & TOP BAR
  // ══════════════════════════════════════════════════════════════
  "sd.nav.courses":    { en: "Courses",              rw: "Amasomo" },
  "sidebar.switchlang":    { en: "Switch Language",      rw: "Hindura Ururimi" },
  "sd.nav.performance":{ en: "Performance",          rw: "Imikorere" },
  "sd.nav.assessments":{ en: "Assessments",          rw: "Ibizamini" },

  // Courses section
  "sd.courses.title":  { en: "All Courses",          rw: "Amasomo Yose" },
  "sd.courses.loading":{ en: "Loading courses…",     rw: "Gukurura amasomo…" },
  "sd.courses.empty":  { en: "No courses available yet.", rw: "Nta masomo aboneka ubu." },
  "sd.courses.enrolled": { en: "✓ Enrolled",         rw: "✓ Wiyandikishije" },
  "sd.courses.modules":{ en: "Modules",              rw: "Ibice" },
  "sd.courses.viewall":{ en: "View all →",           rw: "Reba byose →" },

  // Course enroll page
  "sd.enroll.btn":     { en: "Enroll in Course",     rw: "Iyandikishe" },
  "sd.enroll.enrolled":{ en: "✓ Enrolled",           rw: "✓ Wiyandikishije" },
  "sd.enroll.continue":{ en: "Continue to Course",   rw: "Komeza Isomo" },
  "sd.enroll.back":    { en: "← Back to Courses",    rw: "← Subira ku Masomo" },
  "sd.enroll.guidelines": { en: "Guidelines:",       rw: "Amabwiriza:" },

  // Modules
  "sd.modules.title":  { en: "Course Modules",       rw: "Ibice by'Isomo" },
  "sd.modules.empty":  { en: "No modules yet. Check back later!", rw: "Nta bice bihari ubu. Garuka nyuma!" },
  "sd.modules.lessons":{ en: "lessons",              rw: "amasomo" },
  "sd.modules.lesson": { en: "lesson",               rw: "isomo" },
  "sd.modules.completed":{ en: "completed",          rw: "byarangiye" },
  "sd.modules.alldone":{ en: "All done!",            rw: "Byose byarangiye!" },
  "sd.modules.back":   { en: "← Back to Course",    rw: "← Subira ku Isomo" },

  // Lessons
  "sd.lessons.empty":  { en: "No lessons in this module yet.", rw: "Nta masomo muri iki gice ubu." },
  "sd.lessons.back":   { en: "← Back to Modules",   rw: "← Subira ku Bice" },
  "sd.lessons.markedone": { en: "Marked as Done",   rw: "Byarangiye" },
  "sd.lessons.markdone":  { en: "Mark as Done",     rw: "Ndangije isomo" },
  "sd.lessons.undo":      { en: "Undo",             rw: "Kuraho" },
  "sd.lessons.done.msg":  { en: "You have completed this lesson.", rw: "Urangije iri somo." },
  "sd.lessons.done.hint": { en: "Mark this lesson as done when you're finished.", rw: "Garagaza ko iri somo ryarangiye." },
  "sd.lessons.nofile":    { en: "No file uploaded for this lesson yet. Check back later!", rw: "Nta dosiye yashyizweho kuri iri somo ubu. Garuka nyuma!" },
  "sd.lessons.open":      { en: "Download / Open File", rw: "Fungura Dosiye" },
  "sd.lessons.openpdf":   { en: "Open PDF in new tab",  rw: "Fungura PDF" },
  "sd.lessons.back2":     { en: "← Back to Lessons",   rw: "← Subira ku Masomo" },

  // Performance / Grades
  "sd.perf.title":     { en: "All Grades",           rw: "Amanota Yose" },
  "sd.perf.sub":       { en: "Your assessment results:", rw: "Ibisubizo by'ibizamini byawe:" },
  "sd.perf.overall":   { en: "Overall Grade:",       rw: "Amanota Rusange:" },
  "sd.perf.loading":   { en: "Loading grades…",      rw: "Gushaka amanota…" },
  "sd.perf.empty":     { en: "No grades yet. Complete an assessment to see results here.", rw: "Nta manota ubu. Uzuza ikizamini urebe ibisubizo hano." },
  "sd.perf.graded":    { en: "Graded",               rw: "Imanota Yagaragajwe" },
  "sd.perf.pending":   { en: "Pending review",       rw: "Gitegereje isuzuma" },
  "sd.perf.view":      { en: "View →",               rw: "Reba →" },
  "sd.perf.col.assess":{ en: "Assessment",           rw: "Ikizamini" },
  "sd.perf.col.date":  { en: "Date",                 rw: "Itariki" },
  "sd.perf.col.status":{ en: "Status",               rw: "Imiterere" },
  "sd.perf.col.score": { en: "Score",                rw: "Amanota" },

  // Grade review
  "sd.review.back":    { en: "← Back to Grades",    rw: "← Subira ku Manota" },
  "sd.review.your":    { en: "Your answer:",         rw: "Igisubizo cyawe:" },
  "sd.review.correct": { en: "Correct answer:",      rw: "Igisubizo nyacyo:" },
  "sd.review.points":  { en: "Points:",              rw: "Amanota:" },
  "sd.review.teacher": { en: "Teacher:",             rw: "Umwarimu:" },
  "sd.review.status.correct":  { en: "Correct",      rw: "Nibyo" },
  "sd.review.status.incorrect":{ en: "Incorrect",    rw: "Sibyo" },
  "sd.review.status.pending":  { en: "Pending teacher review", rw: "Gitegereje isuzuma ry'umwarimu" },

  // Assessments
  "sd.quiz.title":     { en: "All Assessments",      rw: "Ibizamini Byose" },
  "sd.quiz.select":    { en: "Select a quiz to start:", rw: "Hitamo ikizamini utangire:" },
  "sd.quiz.empty":     { en: "No assessments available. Enroll in a course to access quizzes.", rw: "Nta bizamini bihari. Iyandikishe kugira ngo ubone ibizamini." },
  "sd.quiz.questions": { en: "Questions",            rw: "Ibibazo" },
  "sd.quiz.remaining": { en: "attempts remaining",   rw: "Usigaje gusubiramo" },
  "sd.quiz.attempt":   { en: "attempt remaining",   rw: "Usigaje gusubiramo" },
  "sd.quiz.neattempt": { en: "No attempts remaining", rw: "Nta gusubiramo" },
  "sd.quiz.best":      { en: "Best:",                rw: "Nziza:" },
  "sd.quiz.minutes":   { en: "min",                  rw: "iminota" },

  // Quiz detail
  "sd.quizd.desc":     { en: "Description:",         rw: "Ibisobanuro:" },
  "sd.quizd.inst":     { en: "Instructions:",        rw: "Amabwiriza:" },
  "sd.quizd.inst1":    { en: "Read each question carefully before answering.", rw: "Soma buri kibazo neza mbere yo gusubiza." },
  "sd.quizd.inst2":    { en: "For multiple-choice questions, select all correct answers.", rw: "Ku bibazo byo guhitamo, hitamo ibisubizo byose nibyo." },
  "sd.quizd.inst3":    { en: "You must answer all questions before submitting.", rw: "Ugomba gusubiza ibibazo byose mbere yo kohereza." },
  "sd.quizd.noattempt":{ en: "No attempts remaining", rw: "Nta gusubiramo" },
  "sd.quizd.used":     { en: "You have used all", rw: "Wamaze gusubiramo" },
  "sd.quizd.attempts": { en: "attempt(s). View your grade in the Performance section.", rw: "wasubiyemo. Reba amanota yawe mu gice cy'Imikorere." },
  "sd.quizd.left":     { en: "attempt(s) remaining. Best score:", rw: "wasubiyemo. Amanota meza:" },
  "sd.quizd.start":    { en: "Start Now",            rw: "Tangira Ubu" },
  "sd.quizd.back":     { en: "← Back to Assessments", rw: "← Subira ku Bizamini" },

  // Quiz session
  "sd.session.question": { en: "Question",           rw: "Ikibazo" },
  "sd.session.of":       { en: "of",                 rw: "kuri" },
  "sd.session.multi":    { en: "Select all correct answers", rw: "Hitamo ibisubizo byose nibyo" },
  "sd.session.short":    { en: "Type your answer here…", rw: "Andika igisubizo cyawe hano…" },
  "sd.session.prev":     { en: "← Previous",         rw: "← Ibanza" },
  "sd.session.next":     { en: "Next →",             rw: "Komeza →" },
  "sd.session.submit":   { en: "Submit Quiz ✓",      rw: "Ohereza Ikizamini ✓" },

  // Quiz result
  "sd.result.title":   { en: "Quiz Completed!",      rw: "Ikizamini Cyarangiye!" },
  "sd.result.score":   { en: "Score",                rw: "Amanota" },
  "sd.result.pending": { en: "on auto-graded questions. Short answers are pending teacher review.", rw: "ku bibazo bisuzumwa vuba. Ibisubizo bigufi bitegereje isuzuma ry'umwarimu." },
  "sd.result.outof":   { en: "out of",               rw: "kuri" },
  "sd.result.points":  { en: "points.",              rw: "amanota." },
  "sd.result.scored":  { en: "You scored",           rw: "Wabonanye" },
  "sd.result.back":    { en: "Back to Assessments",  rw: "Subira ku Bizamini" },
  "sd.result.review":  { en: "Review Answers",       rw: "Suzuma Ibisubizo" },
  "sd.result.grades":  { en: "View My Grades",       rw: "Reba Amanota Yanjye" },

  // ══════════════════════════════════════════════════════════════
  //  TEACHER DASHBOARD — SIDEBAR & TOP BAR
  // ══════════════════════════════════════════════════════════════
  "td.nav.courses":    { en: "Courses",              rw: "Amasomo" },
  "td.nav.performance":{ en: "Performance",          rw: "Imikorere" },
  "td.nav.assessments":{ en: "Assessments",          rw: "Ibizamini" },
  "td.nav.grading":    { en: "Grade Submissions",    rw: "Tanga Amanota" },

  // Courses
  "td.courses.title":  { en: "All Courses",          rw: "Amasomo Yose" },
  "td.courses.create": { en: "+ Create Course",      rw: "+ Shyiraho Isomo" },
  "td.courses.loading":{ en: "Loading courses…",     rw: "Gukurura amasomo…" },
  "td.courses.empty":  { en: "No courses yet. Create your first one!", rw: "Nta masomo ubu. Shyiraho isomo ryawe rya mbere!" },
  "td.courses.modules":{ en: "Modules",              rw: "Ibice" },
  "td.courses.published": { en: "Published",         rw: "Yatangajwe" },
  "td.courses.draft":  { en: "Draft",                rw: "Amakuru yabitswe" },
  "td.courses.edit":   { en: "Edit",                 rw: "Hindura" },
  "td.courses.delete": { en: "Delete",               rw: "Siba" },

  // Create/Edit course form
  "td.form.course.title":   { en: "Create Course",   rw: "Shyiraho Isomo" },
  "td.form.course.edit":    { en: "Edit Course",     rw: "Hindura Isomo" },
  "td.form.course.save":    { en: "Save Changes",    rw: "Bika Impinduka" },
  "td.form.course.publish": { en: "Publish Course",  rw: "Tangaza Isomo" },
  "td.form.course.details": { en: "Course Details",  rw: "Amakuru y'Isomo" },
  "td.form.course.ctitle":  { en: "Course Title:",   rw: "Izina ry'Isomo:" },
  "td.form.course.cdesc":   { en: "Course Description:", rw: "Ibisobanuro by'Isomo:" },
  "td.form.course.guide":   { en: "Guidelines",      rw: "Amabwiriza" },
  "td.form.course.publishnow": { en: "Publish immediately (visible to students)", rw: "Tangaza isomo ako kanya (bibonwa n'abanyeshuri)" },
  "td.form.course.hint":    { en: "You can add more modules and lessons after publishing.", rw: "Ushobora kongeraho ibice n'amasomo nyuma yo gutangaza." },
  "td.form.course.back":    { en: "← Back to Courses", rw: "← Subira ku Masomo" },
  "td.form.module1":        { en: "1. First Module", rw: "1. Igice cya Mbere" },
  "td.form.lesson1":        { en: "2. First Lesson", rw: "2. Isomo rya Mbere" },
  "td.form.modname":        { en: "Module Name:",    rw: "Izina ry'Igice:" },
  "td.form.moddesc":        { en: "Module Description:", rw: "Ibisobanuro by'Igice:" },
  "td.form.lesname":        { en: "Lesson Name:",    rw: "Izina ry'Isomo:" },
  "td.form.filetype":       { en: "File Type:",      rw: "Ubwoko bwa Dosiye:" },
  "td.form.upload":         { en: "Upload File:",    rw: "Ohereza Dosiye:" },
  "td.form.url":            { en: "— or paste a URL —", rw: "— cyangwa shyiramo URL —" },

  // Modules manager
  "td.modules.title":  { en: "Modules & Lessons",   rw: "Ibice n'Amasomo" },
  "td.modules.add":    { en: "+ Add Module",         rw: "+ Ongeraho Igice" },
  "td.modules.empty":  { en: "No modules yet.",      rw: "Nta bice bihari ubu." },
  "td.modules.noles":  { en: "No lessons yet.",      rw: "Nta masomo ubu." },
  "td.modules.uploaded": { en: "File uploaded",      rw: "Dosiye yoherejwe" },
  "td.modules.nofile": { en: "No file yet",          rw: "Nta dosiye ubu" },

  // Add module modal
  "td.modal.modtitle": { en: "Add Module",           rw: "Ongeraho Igice" },
  "td.modal.modname":  { en: "Module Name:",         rw: "Izina ry'Igice:" },
  "td.modal.moddesc":  { en: "Description (optional):", rw: "Ibisobanuro (si ngombwa):" },

  // Add lesson modal
  "td.modal.lestitle": { en: "Add Lesson",           rw: "Ongeraho Isomo" },
  "td.modal.lesname":  { en: "Lesson Name:",         rw: "Izina ry'Isomo:" },
  "td.modal.filetype": { en: "File Type:",           rw: "Ubwoko bwa Dosiye:" },
  "td.modal.upload":   { en: "Upload File:",         rw: "Ohereza Dosiye:" },
  "td.modal.url":      { en: "— or paste a URL instead —", rw: "— cyangwa shyiramo URL aho —" },
  "td.modal.cancel":   { en: "Cancel",               rw: "Hagarika" },
  "td.modal.add":      { en: "Add Module",           rw: "Ongeraho Igice" },
  "td.modal.addmod":   { en: "Add Module",           rw: "Ongeraho Igice" },
  "td.modal.addlesson":{ en: "Add Lesson",           rw: "Ongeraho Isomo" },
  "td.modal.save":     { en: "Save Changes",         rw: "Bika Impinduka" },

  // Edit lesson modal
  "td.modal.edittitle":{ en: "Edit Lesson",          rw: "Hindura Isomo" },
  "td.modal.editlesnm":{ en: "Lesson Name:",         rw: "Izina ry'Isomo:" },
  "td.modal.replace":  { en: "Replace File (optional):", rw: "Hindura Dosiye (si ngombwa):" },
  "td.modal.urlhint":  { en: "— or update URL instead —", rw: "— cyangwa hindura URL aho —" },

  // Delete modal
  "td.modal.cancel2":  { en: "Cancel",               rw: "Hagarika" },

  // Performance
  "td.perf.title":     { en: "Student Performance",  rw: "Imikorere y'Abanyeshuri" },
  "td.perf.sub":       { en: "All enrolled students", rw: "Abanyeshuri bose banditse" },
  "td.perf.export":    { en: "Export Report",        rw: "Sohora Raporo" },
  "td.perf.col.student": { en: "Student",            rw: "Umunyeshuri" },
  "td.perf.col.course":  { en: "Course",             rw: "Isomo" },
  "td.perf.col.status":  { en: "Status",             rw: "Imiterere" },
  "td.perf.col.score":   { en: "Score",              rw: "Amanota" },
  "td.perf.col.enrolled":{ en: "Enrolled",           rw: "Yanditswe" },
  "td.perf.col.view":    { en: "View",               rw: "Reba" },
  "td.perf.empty":     { en: "No enrolled students yet.", rw: "Nta nyeshuri wanditse ubu." },
  "td.perf.loading":   { en: "Loading…",             rw: "Gukurura…" },
  "td.perf.graded":    { en: "Graded",               rw: "Imanota Yagaragajwe" },
  "td.perf.pending":   { en: "Pending review",       rw: "Gitegereje isuzuma" },
  "td.perf.notstarted":{ en: "Not started",          rw: "Nta tangira" },
  "td.perf.submitted": { en: "Submitted",            rw: "Byatanzwe" },

  // Assessments list
  "td.assess.title":   { en: "All Assessments",      rw: "Ibizamini Byose" },
  "td.assess.create":  { en: "+ Create Assessment",  rw: "+ Shyiraho Ikizamini" },
  "td.assess.loading": { en: "Loading…",             rw: "Gukurura…" },
  "td.assess.empty":   { en: "No assessments yet.",  rw: "Nta bizamini bihari" },
  "td.assess.questions": { en: "Questions",          rw: "Ibibazo" },
  "td.assess.locked":  { en: "Locked",               rw: "Ryarangiye" },
  "td.assess.edit":    { en: "Edit",                 rw: "Hindura" },

  // Create/Edit assessment form
  "td.aform.title":    { en: "Create Assessment",    rw: "Shyiraho Ikizamini" },
  "td.aform.edit":     { en: "Edit Assessment",      rw: "Hindura Ikizamini" },
  "td.aform.save":     { en: "Save Assessment",      rw: "Bika Ikizamini" },
  "td.aform.savechanges": { en: "Save Changes",      rw: "Bika Impinduka" },
  "td.aform.details":  { en: "Assessment Details",   rw: "Amakuru y'Ikizamini" },
  "td.aform.atitle":   { en: "Title:",               rw: "Izina:" },
  "td.aform.adesc":    { en: "Description:",         rw: "Ibisobanuro:" },
  "td.aform.course":   { en: "Link to Course:",      rw: "Isomo:" },
  "td.aform.selcourse":{ en: "— Select a course —",  rw: "— Hitamo isomo —" },
  "td.aform.timelimit":{ en: "Time Limit (minutes):", rw: "Igihe ntarengwa (iminota):" },
  "td.aform.maxatt":   { en: "Max Attempts:",        rw: "Gusubiramo byemewe inshuro:" },
  "td.aform.nolimit":  { en: "Leave blank = no limit", rw: "Nta gihe ntarengwa" },
  "td.aform.publish":  { en: "Publish immediately",  rw: "Tangaza ako kanya" },
  "td.aform.questions":{ en: "Questions",            rw: "Ibibazo" },
  "td.aform.addq":     { en: "+ Add Question",       rw: "+ Ongeraho Ikibazo" },
  "td.aform.back":     { en: "← Back to Assessments", rw: "← Subira ku Bizamini" },

  // Question builder
  "td.q.type":         { en: "Question Type:",       rw: "Ubwoko bw'Ikibazo:" },
  "td.q.mcq":          { en: "Multiple Choice",      rw: "Guhitamo Ibisubizo" },
  "td.q.tf":           { en: "True / False",         rw: "Ni Ukuri / Ni Ikinyoma" },
  "td.q.short":        { en: "Short Answer",         rw: "Igisubizo Gifupi" },
  "td.q.text":         { en: "Question Text:",       rw: "Ikibazo:" },
  "td.q.textph":       { en: "Enter question here…", rw: "Andika ikibazo hano…" },
  "td.q.options":      { en: "Answer Options:",      rw: "Ibisubizo Bihitamo:" },
  "td.q.multi":        { en: "Allow multiple correct answers", rw: "Emera ibisubizo bibiri nibyo" },
  "td.q.correct":      { en: "Correct answer:",      rw: "Igisubizo nyacyo:" },
  "td.q.points":       { en: "Points:",              rw: "Amanota:" },
  "td.q.addopt":       { en: "+ Add option",         rw: "+ Ongeraho igisubizo" },
  "td.q.shortdesc":    { en: "Students type a free-text answer. Grade manually in the Grading section.", rw: "Abanyeshuri bandika igisubizo mu magambo. Tanga amanota mu gice cyo Gutanga Amanota." },
  "td.q.correct.lbl":  { en: "Correct",              rw: "Nibyo" },

  // Grading steps
  "td.grade.title":    { en: "Grade Submissions",    rw: "Tanga Amanota" },
  "td.grade.loading":  { en: "Loading pending assessments…", rw: "Gukurura ibizamini bitegereza…" },
  "td.grade.empty":    { en: "No pending submissions to grade. All caught up!", rw: "Nta suzuma ritegereje amanota. Byose byarangiye!" },
  "td.grade.pending":  { en: "pending",              rw: "itegereza" },
  "td.grade.submission":{ en: "submission",          rw: "inyandiko" },
  "td.grade.submissions":{ en: "submissions",        rw: "inyandiko" },
  "td.grade.tograde":  { en: "to grade",             rw: "gutanga amanota" },

  // Grading step 2 — submission list
  "td.grade2.awaiting":{ en: "awaiting grading",     rw: "itegereza amanota" },
  "td.grade2.submitted":{ en: "Submitted:",          rw: "Byatanzwe:" },
  "td.grade2.autoscore":{ en: "Auto-score:",         rw: "Amanota Yikoze:" },
  "td.grade2.pts":     { en: "pts",                  rw: "amanota" },
  "td.grade2.short":   { en: "short answer",         rw: "igisubizo gifupi" },
  "td.grade2.shorts":  { en: "short answers",        rw: "ibisubizo bifupi" },
  "td.grade2.grade":   { en: "Grade",                rw: "Tanga Amanota" },
  "td.grade2.back":    { en: "← Back to Assessments", rw: "← Subira ku Bizamini" },

  // Grading step 3 — single submission
  "td.grade3.grading": { en: "Grading:",             rw: "Gutanga Amanota:" },
  "td.grade3.autoscore":{ en: "Auto-graded:",        rw: "Imanota Yikoze:" },
  "td.grade3.max":     { en: "max",                  rw: "nzura" },
  "td.grade3.noanswer":{ en: "No answer provided",   rw: "Nta gisubizo cyatanzwe" },
  "td.grade3.score":   { en: "Score:",               rw: "Amanota:" },
  "td.grade3.comment": { en: "Optional feedback…",   rw: "Ibitekerezo (si ngombwa)…" },
  "td.grade3.submit":  { en: "Submit Grade",         rw: "Ohereza Amanota" },
  "td.grade3.back":    { en: "← Back to Submissions", rw: "← Subira ku Nyandiko" },

  // Submission review modal
  "td.modal.review.close":  { en: "Close",           rw: "Funga" },
  "td.modal.review.student":{ en: "Your answer:",    rw: "Igisubizo cy'umunyeshuri:" },
  "td.modal.review.correct":{ en: "Correct:",        rw: "Nyacyo:" },
  "td.modal.review.points": { en: "Points:",         rw: "Amanota:" },
  "td.modal.review.comment":{ en: "Comment:",        rw: "Ibitekerezo:" },
  "td.modal.review.none":   { en: "No submissions found.", rw: "Nta nyandiko ibonetse." },

  // ══════════════════════════════════════════════════════════════
  //  SHARED JS ERROR / TOAST MESSAGES
  // ══════════════════════════════════════════════════════════════
  "err.required.name":  { en: "Full name is required.",  rw: "Amazina arasabwa." },
  "err.required.email": { en: "Email is required.",      rw: "Imeyili irasabwa." },
  "err.required.pass":  { en: "Password is required.",   rw: "Ijambo ry'ibanga rirasabwa." },
  "err.otp.length":     { en: "Enter the 6-digit code.", rw: "Injiza umubare w'imibare 6." },
  "err.login.failed":   { en: "Login failed.",           rw: "Kwinjira ntibyakunze." },
  "err.reg.failed":     { en: "Registration failed.",    rw: "Kwiyandikisha ntibyakunze." },
  "err.notteacher":     { en: "This account is not a teacher account.", rw: "Iyi konti si iya umwarimu." },
  "err.course.title":   { en: "Enter a course title.",   rw: "Injiza izina ry'isomo." },
  "err.module.name":    { en: "Enter a module name.",    rw: "Injiza izina ry'igice." },
  "err.lesson.name":    { en: "Enter a lesson name.",    rw: "Injiza izina ry'isomo." },
  "err.lesson.file":    { en: "Please upload a file or enter a URL.", rw: "Ohereza dosiye cyangwa injiza URL." },
  "err.assess.title":   { en: "Enter an assessment title.", rw: "Injiza izina ry'ikizamini." },
  "err.assess.course":  { en: "Select a course.",        rw: "Hitamo isomo." },
  "err.q.text":         { en: "All questions need text.", rw: "Ibibazo byose bikeneye ikibazo." },
  "err.q.options":      { en: "MCQ needs at least 2 options.", rw: "Guhitamo gusaba nibura ibisubizo 2." },
  "err.q.correct":      { en: "Mark at least one correct answer.", rw: "Shyira ikimenyetso ku gisubizo kimwe nibyo." },
  "err.q.tf":           { en: "Select True or False for each T/F question.", rw: "Hitamo Ni Ukuri cyangwa Ni Ikinyoma kuri buri kibazo." },
  "err.q.atleast":      { en: "Add at least one question.", rw: "Ongeraho nibura ikibazo kimwe." },
  "err.load.course":    { en: "Failed to load course.",  rw: "Gukunura isomo ntibishoboye." },
  "err.load.assess":    { en: "Failed to load assessment.", rw: "Kutabasha gukurura ikizamini." },
  "err.grade.fail":     { en: "Failed to submit grade.", rw: "Kutabasha kohereza amanota." },
  "err.enroll.fail":    { en: "Enrollment failed.",      rw: "Kwiyandikisha ntibyakunze." },
  "err.submit.fail":    { en: "Submission failed.",      rw: "Kohereza ntibyakunze." },

  "toast.welcome":      { en: "Welcome back!",            rw: "Murakaza neza!" },
  "toast.created":      { en: "Account created! Check your email.", rw: "Konti yarakozwe! Reba imeyili yawe." },
  "toast.verified":     { en: "Email verified! Redirecting…", rw: "Imeyili yemejwe! Uzengurutswa…" },
  "toast.code.sent":    { en: "New code sent!",           rw: "Kode nshya yoherejwe!" },
  "toast.code.failed":  { en: "Could not resend.",        rw: "Ntibishoboye kohereza." },
  "toast.course.saved": { en: "Course created!",          rw: "Isomo ryashyizweho!" },
  "toast.course.updated":{ en: "Course updated!",         rw: "Isomo ryahinduwe!" },
  "toast.course.deleted":{ en: "Course deleted.",         rw: "Isomo ryasibwe." },
  "toast.module.added": { en: "Module added!",            rw: "Igice cyongeweho!" },
  "toast.lesson.added": { en: "Lesson added!",            rw: "Isomo ryongeweho!" },
  "toast.lesson.updated":{ en: "Lesson updated!",         rw: "Isomo ryahinduwe!" },
  "toast.lesson.done":  { en: "Lesson marked as done! ✓", rw: "Isomo ryagaragajwe nk'iryarangiye! ✓" },
  "toast.lesson.undone":{ en: "Lesson unmarked.",         rw: "Isomo ryagaragajwe nk'iritararangira X." },
  "toast.assess.saved": { en: "Assessment saved!",        rw: "Ikizamini cyabitswe!" },
  "toast.assess.updated":{ en: "Assessment updated!",     rw: "Ikizamini cyahinduwe!" },
  "toast.grade.done":   { en: "Grade submitted!",         rw: "Amanota yoherejwe!" },
  "toast.enrolled":     { en: "Enrolled successfully!",   rw: "Wiyandikishije neza!" },
  "toast.pdf.gen":      { en: "Generating PDF…",          rw: "Gukora PDF…" },
  "toast.delete.done":  { en: "Deleted.",                 rw: "Byasibwe." },
  "toast.delete.fail":  { en: "Delete failed.",           rw: "Gusiba ntibyakunze." },
};

// ── Language management ───────────────────────────────────────────────────────
function getLang() {
  return localStorage.getItem('iga_lang') || 'en';
}

function setLang(lang) {
  localStorage.setItem('iga_lang', lang);
  applyLang();
  const label = lang === 'en' ? 'EN' : 'RW';
  const navLabel  = document.getElementById('langLabel');
  const footLabel = document.getElementById('footerLangLabel');
  if (navLabel)  navLabel.textContent  = label;
  if (footLabel) footLabel.textContent = label;
  document.dispatchEvent(new CustomEvent('iga-lang-changed', { detail: { lang } }));
}

function toggleLang() {
  setLang(getLang() === 'en' ? 'rw' : 'en');
}

function applyLang() {
  const lang = getLang();
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const v = TRANSLATIONS[el.dataset.i18n];
    if (v && v[lang]) el.textContent = v[lang];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const v = TRANSLATIONS[el.dataset.i18nPlaceholder];
    if (v && v[lang]) el.placeholder = v[lang];
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const v = TRANSLATIONS[el.dataset.i18nHtml];
    if (v && v[lang]) el.innerHTML = v[lang];
  });
}

/** Translate a key in JS code: t('toast.welcome') */
function t(key) {
  const lang = getLang();
  const v = TRANSLATIONS[key];
  return (v && v[lang]) ? v[lang] : key;
}

// Auto-apply on every page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', applyLang);
} else {
  applyLang();
}

// Expose globally so onclick="toggleLang()" in injected HTML always works
window.toggleLang = toggleLang;
window.setLang    = setLang;
window.getLang    = getLang;
window.applyLang  = applyLang;
window.t          = t;