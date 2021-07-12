float4 Main(float4 p_viewport : SV_Position) : SV_Target
{
    float4 color;
    color[0u] = 0.0f;
    color[1u] = 1.0f;
    color[2u] = 2.0f;
    color[3u] = 3.0f;
    // color[4u] = 4.0f; out-of-bounds error
    
    return color;
}
