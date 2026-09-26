-- Development-only generic prompts; these are placeholders, not the real RUDAS.
INSERT INTO assessment_items (id, assessment_key, item_number, prompt, response_options, version, language)
VALUES
('50000000-0000-4000-8000-000000000001', 'rudas', 1, 'Placeholder item 1 (not the real RUDAS)', '["Response A", "Response B", "Response C"]', 'placeholder-v1', 'en'),
('50000000-0000-4000-8000-000000000002', 'rudas', 2, 'Placeholder item 2 (not the real RUDAS)', '["Response A", "Response B", "Response C"]', 'placeholder-v1', 'en'),
('50000000-0000-4000-8000-000000000003', 'rudas', 3, 'Placeholder item 3 (not the real RUDAS)', '["Response A", "Response B", "Response C"]', 'placeholder-v1', 'en'),
('50000000-0000-4000-8000-000000000004', 'rudas', 4, 'Placeholder item 4 (not the real RUDAS)', '["Response A", "Response B", "Response C"]', 'placeholder-v1', 'en'),
('50000000-0000-4000-8000-000000000005', 'rudas', 5, 'Placeholder item 5 (not the real RUDAS)', '["Response A", "Response B", "Response C"]', 'placeholder-v1', 'en'),
('50000000-0000-4000-8000-000000000006', 'rudas', 6, 'Placeholder item 6 (not the real RUDAS)', '["Response A", "Response B", "Response C"]', 'placeholder-v1', 'en')
ON CONFLICT (assessment_key, item_number, version, language) DO NOTHING;