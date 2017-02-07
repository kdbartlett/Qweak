SELECT bm.run_number AS 'Run #', 
			bm.slug AS 'Slug', 
			bm.wien_slug AS 'Wien', 
			sc.target_position AS 'Target', 
			ROUND(MAX(bm.value),0) AS 'Beam Current', 
			ROUND(MAX(sc.qtor_current),0) AS 'QTor Current', 
			sc.slow_helicity_plate AS 'IHWP1', 
			sc.passive_helicity_plate AS 'IHWP2' 
FROM beam_view AS bm 
LEFT JOIN slow_controls_settings AS sc ON bm.runlet_id=sc.runlet_id 
WHERE sc.target_position='DS-4%-Aluminum' AND bm.monitor='qwk_bcm8' AND bm.value > 0
GROUP BY bm.run_number;
