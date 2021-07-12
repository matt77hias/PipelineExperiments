static const uint g_count = 4u;

float4 Main(float4 p_viewport : SV_Position) : SV_Target
{
    const vector< float, g_count > src = 7.0f;
    const float4 dst = src;
    
    return dst;
}
