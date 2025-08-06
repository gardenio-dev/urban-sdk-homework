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
	"length" NUMERIC,
	"geom" Geometry(LineString, 4326)
);
CREATE INDEX idx_links_geom ON "traffic"."links" USING GIST(geom);

-- Create the "speed_records" table.
DROP TABLE IF EXISTS "traffic"."speed_records";
CREATE TABLE IF NOT EXISTS "traffic"."speed_records"(
	"id" SERIAL PRIMARY KEY,
	"link_id" BIGINT REFERENCES "traffic"."links"("link_id"),
	"speed" DOUBLE PRECISION,
	"day_of_week" SMALLINT,
	"period" SMALLINT,
	"timestamp" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_speed_records_link_id ON "traffic"."speed_records"("link_id");
CREATE INDEX IF NOT EXISTS idx_speed_records_speed ON "traffic"."speed_records"("speed");
CREATE INDEX IF NOT EXISTS idx_speed_records_day_of_week ON "traffic"."speed_records"("day_of_week");
CREATE INDEX IF NOT EXISTS idx_speed_records_period ON "traffic"."speed_records"("period");
CREATE INDEX IF NOT EXISTS idx_speed_records_timestamp ON "traffic"."speed_records"("timestamp");

-- ETL the Links data.
DELETE FROM "traffic"."links";
INSERT INTO
	"traffic"."links"(
		"link_id",
		"road_name",
		"length",
		"geom"
	)
SELECT
	"link_id",
	"road_name",
	"_length",
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
DELETE FROM "traffic"."speed_records";
INSERT INTO
	"traffic"."speed_records"(
		"link_id",
		"speed",
		"day_of_week",
		"period",
		"timestamp"
	)
SELECT
	"link_id",
	"average_speed",
	"day_of_week",
	"period",
	"date_time"::TIMESTAMPTZ
FROM
	"staging"."duval_jan1_2024"
;
