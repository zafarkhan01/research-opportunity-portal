USE research_portal;

INSERT INTO opportunities
(title, description, research_area, faculty_name, department, required_skills, positions, deadline, status)
VALUES
('Machine Learning for Crop Disease Detection',
 'Build image classification models to detect crop diseases.',
 'Machine Learning', 'Dr. Ahmed Khan', 'Computer Science',
 'Python, TensorFlow, Image Processing', 2, '2026-12-31', 'Open'),

('Network Traffic Anomaly Detection',
 'Analyze network traffic to detect unusual patterns.',
 'Computer Networks', 'Dr. Sara Ali', 'Computer Science',
 'Python, Wireshark, Data Analysis', 3, '2026-12-15', 'Open'),

('Natural Language Processing for Urdu',
 'Develop text processing tools for the Urdu language.',
 'NLP', 'Dr. Usman Raza', 'Artificial Intelligence',
 'Python, NLP, Linguistics', 1, '2026-11-30', 'Open');