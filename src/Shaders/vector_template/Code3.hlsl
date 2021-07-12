static const uint g_count = 1u;

float4 Main(float4 p_viewport : SV_Position) : SV_Target
{
    vector< float, g_count > src = 7.0f;
    float dst = src;
    
    // dst[0u] = src; error
    src[0u] = dst;
    
    return dst;
}
