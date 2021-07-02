static const uint3 g_group_thread_count = uint3(8u, 8u, 1u);

[numthreads(g_group_thread_count.x,
            g_group_thread_count.y,
            g_group_thread_count.z)]
void Main(uint3 dispatch_thread_id : SV_DispatchThreadID)
{}
