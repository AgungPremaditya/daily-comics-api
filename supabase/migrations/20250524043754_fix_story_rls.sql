-- First, disable RLS since we're not using authentication yet
ALTER TABLE "public"."story" DISABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations (just in case RLS is re-enabled in the future)
DROP POLICY IF EXISTS "Enable all operations for all users" ON "public"."story";
CREATE POLICY "Enable all operations for all users" ON "public"."story"
    FOR ALL
    TO public
    USING (true)
    WITH CHECK (true); 