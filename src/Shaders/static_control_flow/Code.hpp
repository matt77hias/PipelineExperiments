static const bool g_flag = true;

float4 Main(float4 p_viewport : SV_Position) : SV_Target
{
    if (g_flag)
    {
        return 7.0f;
    }
    else
    {
        return 9.0f;
    }
}
