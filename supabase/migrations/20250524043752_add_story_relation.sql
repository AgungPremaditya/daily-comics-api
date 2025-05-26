-- Add story_id column to comics table if it doesn't exist
ALTER TABLE "public"."comics" ADD COLUMN IF NOT EXISTS "story_id" bigint;

-- Add foreign key constraint
ALTER TABLE "public"."comics" 
ADD CONSTRAINT "comics_story_id_fkey" 
FOREIGN KEY ("story_id") 
REFERENCES "public"."story"("id") 
ON DELETE CASCADE; 