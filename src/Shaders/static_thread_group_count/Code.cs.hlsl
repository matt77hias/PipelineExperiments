static const uint g_group_thread_count_x = 8u;
static const uint g_group_thread_count_y = 8u;
static const uint g_group_thread_count_z = 1u;

[numthreads(g_group_thread_count_x,
            g_group_thread_count_y,
            g_group_thread_count_z)]
void Main(uint3 dispatch_thread_id : SV_DispatchThreadID)
{}
