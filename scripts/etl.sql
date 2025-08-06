-- Make sure we're ready to handle geometry.
CREATE EXTENSION IF NOT EXISTS postgis;
-- Create the "traffic" schema.
CREATE SCHEMA IF NOT EXISTS "traffic";

-- Create the "links" table.
DROP TABLE IF EXISTS "traffic"."links" CASCADE;
CREATE TABLE IF NOT EXISTS "traffic"."links"(
	-- "link_id" wouldn't be the first choice for the ID column
	-- on a relation called "links"... but this seems more consistent
	-- with the assignment.
	"link_id" BIGINT PRIMARY KEY,
	"road_name" CHARACTER VARYING,
	"geom" Geometry(LineString, 4326)
);
CREATE INDEX idx_links_geom ON "traffic"."links" USING GIST(geom);

-- Create the "link aggregates" table.
DROP TABLE IF EXISTS "traffic"."link_aggs";
CREATE TABLE IF NOT EXISTS "traffic"."link_aggs"(
	"id" SERIAL PRIMARY KEY,
	"link_id" BIGINT REFERENCES "traffic"."links"("link_id"),
	"average_speed" DOUBLE PRECISION,
	"day_of_week" SMALLINT,
	"period" SMALLINT
);
CREATE INDEX IF NOT EXISTS idx_link_aggs_link_id ON "traffic"."link_aggs"("link_id");
CREATE INDEX IF NOT EXISTS idx_link_aggs_average_speed ON "traffic"."link_aggs"("average_speed");
CREATE INDEX IF NOT EXISTS idx_link_aggs_day_of_week ON "traffic"."link_aggs"("day_of_week");
CREATE INDEX IF NOT EXISTS idx_link_aggs_period ON "traffic"."link_aggs"("period");

-- ETL the Links data.
DELETE FROM "traffic"."links";
INSERT INTO 
	"traffic"."links"(
		"link_id",
		"road_name",
		"geom"
	)
SELECT
	"link_id",
	"road_name",
	ST_SetSRID(
		ST_GeometryN(  -- The data came in as MultiLinestring.
			ST_GeomFromGeoJSON(
				"geo_json"
			),
			1
		),
		4326
	)
FROM
	"staging"."link_info"
;

-- ETL the aggregates data.
DELETE FROM "traffic"."link_aggs";
INSERT INTO 
	"traffic"."link_aggs"(
		"link_id",
		"average_speed",
		"day_of_week",
		"period"
	)
SELECT
	"link_id",
	"average_speed",
	"day_of_week",
	"period"
FROM
	"staging"."duval_jan1_2024"
;


