"""Configuration Phase Router."""

import secrets
from logging import getLogger

from nbtlib import (
    Byte,
    Compound,
    Double,
    Float,
    Int,
    List,
    String,
)

from pythonium.engine import Client, Router
from pythonium.engine.enums import State
from pythonium.engine.enums.teleport_flags import TeleportFlags
from pythonium.engine.packets import (
    AcknowledgeFinishConfiguration,
    ClientInformation,
    ConfigurationCustomPayload,
    FinishConfiguration,
    KeepAliveConfigurationRequest,
    KeepAliveConfigurationResponse,
    Login,
    PingConfiguration,
    PongConfiguration,
    RegistryData,
    SetDefaultSpawnPosition,
    SynchronizePlayerPosition,
)
from pythonium.engine.packets.base import Packet

logger = getLogger(__name__)
router = Router(name=__name__)


@router.on(ClientInformation)
async def on_client_information(
    client_information: ClientInformation, client: Client
) -> tuple[Packet, ...]:
    client.session.locale = client_information.locale
    client.session.view_distance = client_information.view_distance
    client.session.chat_mode = client_information.chat_mode
    client.session.chat_colors = client_information.chat_colors
    client.session.displayed_skin_parts = (
        client_information.displayed_skin_parts
    )
    client.session.main_hand = client_information.main_hand
    client.session.enable_text_filtering = (
        client_information.enable_text_filtering
    )
    client.session.allow_server_listings = (
        client_information.allow_server_listings
    )
    client.session.particle_status = client_information.particle_status

    def dmg(
        msg_id: str,
        exhaustion: float = 0.1,
        scaling: str = "always",
        effects: str = "hurt",
        death_msg: str = "default",
    ) -> Compound:
        return Compound(
            {
                "message_id": String(msg_id),
                "exhaustion": Float(exhaustion),
                "scaling": String(scaling),
                "effects": String(effects),
                "death_message_type": String(death_msg),
            }
        )

    default_spawn_conditions = List([Compound({"priority": Int(1)})])

    overworld_dim = Compound(
        {
            "has_skylight": Byte(1),
            "has_ceiling": Byte(0),
            "ultrawarm": Byte(0),
            "natural": Byte(1),
            "coordinate_scale": Double(1.0),
            "bed_works": Byte(1),
            "respawn_anchor_works": Byte(0),
            "min_y": Int(-64),
            "height": Int(384),
            "logical_height": Int(384),
            "infiniburn": String("#minecraft:infiniburn_overworld"),
            "effects": String("minecraft:overworld"),
            "ambient_light": Float(0.0),
            "piglin_safe": Byte(0),
            "has_raids": Byte(1),
            "monster_spawn_light_level": Int(0),
            "monster_spawn_block_light_limit": Int(0),
        }
    )

    cat_tabby = Compound(
        {
            "asset_id": String("minecraft:textures/entity/cat/tabby.png"),
            "spawn_conditions": default_spawn_conditions,
        }
    )

    chicken_normal = Compound(
        {
            "asset_id": String("minecraft:textures/entity/chicken.png"),
            "model": String("normal"),
            "spawn_conditions": default_spawn_conditions,
        }
    )

    cow_normal = Compound(
        {
            "asset_id": String("minecraft:textures/entity/cow/cow.png"),
            "model": String("normal"),
            "spawn_conditions": default_spawn_conditions,
        }
    )

    frog_temperate = Compound(
        {
            "asset_id": String(
                "minecraft:textures/entity/frog/temperate_frog.png"
            ),
            "spawn_conditions": default_spawn_conditions,
        }
    )

    pig_normal = Compound(
        {
            "asset_id": String("minecraft:textures/entity/pig/pig.png"),
            "model": String("normal"),
            "spawn_conditions": default_spawn_conditions,
        }
    )

    wolf_pale = Compound(
        {
            "assets": Compound(
                {
                    "wild": String("minecraft:textures/entity/wolf/wolf.png"),
                    "tame": String(
                        "minecraft:textures/entity/wolf/wolf_tame.png"
                    ),
                    "angry": String(
                        "minecraft:textures/entity/wolf/wolf_angry.png"
                    ),
                }
            ),
            "spawn_conditions": default_spawn_conditions,
        }
    )

    wolf_sound_classic = Compound(
        {
            "ambient_sound": String("minecraft:entity.wolf.ambient"),
            "death_sound": String("minecraft:entity.wolf.death"),
            "growl_sound": String("minecraft:entity.wolf.growl"),
            "hurt_sound": String("minecraft:entity.wolf.hurt"),
            "pant_sound": String("minecraft:entity.wolf.pant"),
            "whine_sound": String("minecraft:entity.wolf.whine"),
        }
    )

    nautilus_normal = Compound(
        {
            "asset_id": String("minecraft:textures/entity/zombie/zombie.png"),
            "model": String("normal"),
            "spawn_conditions": default_spawn_conditions,
        }
    )

    plains_biome = Compound(
        {
            "has_precipitation": Byte(1),
            "temperature": Float(0.8),
            "downfall": Float(0.4),
            "effects": Compound(
                {
                    "fog_color": Int(12638463),
                    "water_color": Int(4159204),
                    "water_fog_color": Int(329011),
                    "sky_color": Int(7907327),
                }
            ),
        }
    )

    damage_type_entries = [
        (
            "minecraft:arrow",
            dmg("arrow", 0.1, "when_caused_by_living_non_player"),
        ),
        (
            "minecraft:bad_respawn_point",
            dmg(
                "badRespawnPoint",
                scaling="always",
                death_msg="intentional_game_design",
            ),
        ),
        ("minecraft:cactus", dmg("cactus", 0.1, "always")),
        ("minecraft:campfire", dmg("campfire", 0.1, "always")),
        ("minecraft:cramming", dmg("cramming", 0.0, "never")),
        ("minecraft:dragon_breath", dmg("dragonBreath", 0.0, "never")),
        ("minecraft:drown", dmg("drown", 0.0, "never", effects="drowning")),
        ("minecraft:dry_out", dmg("dryOut", 0.1, "always")),
        ("minecraft:ender_pearl", dmg("fallback", 0.0, "never")),
        ("minecraft:explosion", dmg("explosion", 0.1, "always")),
        (
            "minecraft:fall",
            dmg("fall", 0.0, "always", death_msg="fall_variants"),
        ),
        ("minecraft:falling_anvil", dmg("anvil", 0.1, "always")),
        ("minecraft:falling_block", dmg("fallingBlock", 0.1, "always")),
        (
            "minecraft:falling_stalactite",
            dmg("fallingStalactite", 0.1, "always"),
        ),
        (
            "minecraft:fireball",
            dmg(
                "fireball",
                0.1,
                "when_caused_by_living_non_player",
                effects="burning",
            ),
        ),
        ("minecraft:fireworks", dmg("fireworks", 0.1, "always")),
        ("minecraft:fly_into_wall", dmg("flyIntoWall", 0.0, "always")),
        ("minecraft:freeze", dmg("freeze", 0.0, "never", effects="freezing")),
        ("minecraft:generic", dmg("generic", 0.0, "never")),
        ("minecraft:generic_kill", dmg("genericKill", 0.0, "never")),
        ("minecraft:hot_floor", dmg("hotFloor", 0.1, "always")),
        ("minecraft:in_fire", dmg("inFire", 0.1, "always", effects="burning")),
        ("minecraft:in_wall", dmg("inWall", 0.0, "never")),
        ("minecraft:indirect_magic", dmg("indirectMagic", 0.0, "never")),
        ("minecraft:lava", dmg("lava", 0.1, "always", effects="burning")),
        ("minecraft:lightning_bolt", dmg("lightningBolt", 0.1, "always")),
        ("minecraft:mace_smash", dmg("mace_smash", 0.1, "always")),
        ("minecraft:magic", dmg("magic", 0.0, "never")),
        ("minecraft:mob_attack", dmg("mob", 0.1, "always")),
        ("minecraft:mob_attack_no_aggro", dmg("mob", 0.1, "always")),
        (
            "minecraft:mob_projectile",
            dmg("mob", 0.1, "when_caused_by_living_non_player"),
        ),
        ("minecraft:on_fire", dmg("onFire", 0.0, "never", effects="burning")),
        ("minecraft:out_of_world", dmg("outOfWorld", 0.0, "never")),
        ("minecraft:outside_border", dmg("outsideBorder", 0.0, "never")),
        ("minecraft:player_attack", dmg("player", 0.1, "always")),
        ("minecraft:player_explosion", dmg("explosion.player", 0.1, "always")),
        ("minecraft:sonic_boom", dmg("sonic_boom", 0.0, "always")),
        (
            "minecraft:spit",
            dmg("mob", 0.1, "when_caused_by_living_non_player"),
        ),
        ("minecraft:stalagmite", dmg("stalagmite", 0.0, "always")),
        ("minecraft:starve", dmg("starve", 0.0, "never")),
        ("minecraft:sting", dmg("sting", 0.1, "always")),
        (
            "minecraft:sweet_berry_bush",
            dmg("sweetBerryBush", 0.1, "always", effects="poking"),
        ),
        ("minecraft:thorns", dmg("thorns", 0.1, "never", effects="thorns")),
        (
            "minecraft:thrown",
            dmg("thrown", 0.1, "when_caused_by_living_non_player"),
        ),
        (
            "minecraft:trident",
            dmg("trident", 0.1, "when_caused_by_living_non_player"),
        ),
        (
            "minecraft:unattributed_fireball",
            dmg("onFire", 0.1, "always", effects="burning"),
        ),
        ("minecraft:wind_charge", dmg("wind_charge", 0.1, "always")),
        ("minecraft:wither", dmg("wither", 0.0, "never")),
        (
            "minecraft:wither_skull",
            dmg("witherSkull", 0.1, "when_caused_by_living_non_player"),
        ),
    ]

    painting_kebab = Compound(
        {
            "asset_id": String("minecraft:kebab"),
            "width": Int(1),
            "height": Int(1),
            "title": String('{"text":"Kebab"}'),
            "author": String('{"text":"ZezuzL0L"}'),
        }
    )

    return (
        RegistryData(
            registry_id="minecraft:dimension_type",
            entries=[("minecraft:overworld", overworld_dim)],
        ),
        RegistryData(
            registry_id="minecraft:worldgen/biome",
            entries=[("minecraft:plains", plains_biome)],
        ),
        RegistryData(
            registry_id="minecraft:damage_type",
            entries=damage_type_entries,
        ),
        RegistryData(
            registry_id="minecraft:cat_variant",
            entries=[("minecraft:tabby", cat_tabby)],
        ),
        RegistryData(
            registry_id="minecraft:chicken_variant",
            entries=[("minecraft:normal", chicken_normal)],
        ),
        RegistryData(
            registry_id="minecraft:cow_variant",
            entries=[("minecraft:normal", cow_normal)],
        ),
        RegistryData(
            registry_id="minecraft:frog_variant",
            entries=[("minecraft:temperate", frog_temperate)],
        ),
        RegistryData(
            registry_id="minecraft:pig_variant",
            entries=[("minecraft:normal", pig_normal)],
        ),
        RegistryData(
            registry_id="minecraft:wolf_variant",
            entries=[("minecraft:pale", wolf_pale)],
        ),
        RegistryData(
            registry_id="minecraft:wolf_sound_variant",
            entries=[("minecraft:classic", wolf_sound_classic)],
        ),
        RegistryData(
            registry_id="minecraft:zombie_nautilus_variant",
            entries=[("minecraft:normal", nautilus_normal)],
        ),
        RegistryData(
            registry_id="minecraft:painting_variant",
            entries=[("minecraft:kebab", painting_kebab)],
        ),
        PingConfiguration(
            id_=secrets.randbelow(2**31 - 1),
        ),
    )


@router.on(KeepAliveConfigurationRequest)
async def on_login(
    keep_alive: KeepAliveConfigurationRequest,
) -> KeepAliveConfigurationResponse:
    return KeepAliveConfigurationResponse(
        keep_alive_id=keep_alive.keep_alive_id
    )


@router.on(PongConfiguration)
async def on_pong(
    _pong: PongConfiguration,
) -> FinishConfiguration:
    return FinishConfiguration()


@router.on(ConfigurationCustomPayload)
async def on_payload(
    payload: ConfigurationCustomPayload,
) -> None: ...


@router.on(AcknowledgeFinishConfiguration)
async def on_finish_configuration(
    _payload: AcknowledgeFinishConfiguration, client: Client
) -> tuple[Packet, ...]:
    client.session.state = State.PLAY

    return (
        Login(
            entity_id=1,
            is_hardcore=False,
            dimension_names=["minecraft:overworld"],
            max_players=100,
            view_distance=10,
            simulation_distance=10,
            reduced_debug_info=False,
            enable_respawn_screen=True,
            do_limited_crafting=False,
            dimension_type=0,
            dimension_name="minecraft:overworld",
            hashed_seed=0,
            game_mode=0,
            previous_game_mode=-1,
            is_debug=False,
            is_flat=False,
            has_death_location=False,
            portal_cooldown=0,
        ),
        SetDefaultSpawnPosition(
            spawn_position=(0, 10, 0),
            angle=0.0,
        ),
        SynchronizePlayerPosition(
            teleport_id=0,
            x=0,
            y=10,
            z=10,
            velocity_x=0.0,
            velocity_y=0.0,
            velocity_z=0.0,
            yaw=0.0,
            pitch=0.0,
            flags=TeleportFlags.relative_pitch,
        ),
    )
